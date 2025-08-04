import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, quote_plus
import random
import re
import pandas as pd
import os
import boto3
from loguru import logger
from io import StringIO
from benchmarking.benchmarking_job import run_benchmarking_job
import datetime
from io import BytesIO
EXPORT_S3_BUCKET = os.getenv("EXPORT_S3_BUCKET", "sai-genai-data-export")

class ComprehensiveScraper:
    def __init__(self, domain="amazon.in"):
        """
        Comprehensive Amazon scraper focused on unit price extraction
        domain: "amazon.in" for India or "amazon.ae" for UAE
        """
        self.domain = domain
        self.base_url = f"https://www.{domain}"
        
        # Currency mapping for different domains
        self.currency_info = {
            "amazon.in": {"symbol": "₹", "code": "INR", "name": "Indian Rupee"},
            "amazon.ae": {"symbol": "AED", "code": "AED", "name": "UAE Dirham"}
        }
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]

    def get_headers(self):
        """Get randomized headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }

    async def search_products(self, search_query, num_pages=3):
        """Search for products across multiple pages"""
        logger.info(f"🔍 Searching for '{search_query}' on {self.domain}")
        logger.info(f"📄 Will scrape {num_pages} pages")
        
        all_products = []
        
        async with AsyncWebCrawler(
            headless=True,
            verbose=True,
            browser_type="chromium",
            delay_between_requests=3
        ) as crawler:
            
            for page in range(1, num_pages + 1):
                logger.info(f"\n📄 Scraping page {page}...")
                
                encoded_query = quote_plus(search_query)
                search_url = f"{self.base_url}/s?k={encoded_query}&page={page}&ref=sr_pg_{page}"
                
                try:
                    result = await crawler.arun(
                        url=search_url,
                        headers=self.get_headers(),
                        wait_for_selector="[data-component-type], .s-result-item, [data-asin]",
                        delay_before_return_html=5
                    )
                    
                    if result.success and result.html:
                        soup = BeautifulSoup(result.html, 'html.parser')
                        
                        if self._is_blocked(soup):
                            logger("❌ Detected blocking. Waiting...")
                            await asyncio.sleep(10)
                            continue
                        
                        page_products = self._extract_search_results(soup, page)
                        all_products.extend(page_products)
                        
                        logger.info(f"✓ Found {len(page_products)} products on page {page}")
                    else:
                        logger.info(f"✗ Failed to load page {page}")
                        
                except Exception as e:
                    logger.error(f"❌ Error on page {page}: {str(e)}")
                
                # Human-like delay
                delay = random.uniform(4, 8)
                await asyncio.sleep(delay)
        
        logger.info(f"\n🎉 Total products found: {len(all_products)}")
        return all_products

    def _is_blocked(self, soup):
        """Check if we're being blocked by Amazon"""
        if soup.find('form', {'action': '/errors/validateCaptcha'}):
            return True
        
        text = soup.get_text().lower()
        blocking_indicators = ['robot or human', 'captcha', 'enter the characters']
        return any(indicator in text for indicator in blocking_indicators)

    def _extract_search_results(self, soup, page_num):
        """Extract basic product info from search results"""
        products = []
        
        container_selectors = [
            "[data-component-type='s-search-result']",
            ".s-result-item[data-asin]",
            "[data-asin]:not([data-asin=''])"
        ]
        
        containers = []
        for selector in container_selectors:
            containers = soup.select(selector)
            if containers:
                logger.info(f"✓ Using selector: {selector} ({len(containers)} products)")
                break
        
        for i, container in enumerate(containers[:20]):
            try:
                asin = container.get('data-asin', '')
                if not asin:
                    continue
                
                product_url = f"{self.base_url}/dp/{asin}"
                
                # Extract title
                title = None
                title_selectors = [
                    "h2 a span", "h2 span", ".a-link-normal span", 
                    "[data-cy='title-recipe']", "a[href*='/dp/'] span"
                ]
                
                for title_sel in title_selectors:
                    title_elem = container.select_one(title_sel)
                    if title_elem and title_elem.get_text(strip=True):
                        title = title_elem.get_text(strip=True)
                        break
                
                if not title:
                    continue
                
                product = {
                    "asin": asin,
                    "url": product_url,
                    "title": title,
                    "search_price": self._extract_price(container),
                    "image": self._extract_image(container),
                    "rating": self._extract_rating(container),
                    "page": page_num,
                    "position": i + 1
                }
                
                products.append(product)
                
            except Exception as e:
                logger.error(f"Error extracting product {i}: {e}")
                continue
        
        return products


    async def get_comprehensive_product_details(
    self,
    product_urls,
    workspace_id,
    secret_name,
    region_name,
    benchmarking_row_id,
    cluster_id=None,     
    query=None           
):
        """
        Get COMPREHENSIVE product details with UNIT PRICE as main focus and save full CSV
        """
        if not product_urls:
            return []

        if isinstance(product_urls[0], dict):
            urls_to_process = [(p["url"], p) for p in product_urls]
        else:
            urls_to_process = [(url, {}) for url in product_urls]

        logger.info(f"\n🔍 Getting COMPREHENSIVE details for {len(urls_to_process)} products...")
        logger.info("🎯 PRIMARY FOCUS: Unit Price Information")

        detailed_products = []

        async with AsyncWebCrawler(
            headless=True,
            verbose=False,
            delay_between_requests=3
        ) as crawler:

            for i, (url, basic_info) in enumerate(urls_to_process, 1):
                logger.info(f"\n📦 Processing product {i}/{len(urls_to_process)}")
                logger.info(f"🔗 URL: {url}")

                try:
                    result = await crawler.arun(
                        url=url,
                        headers=self.get_headers(),
                        wait_for_selector="#productTitle, #title",
                        delay_before_return_html=4
                    )

                    if result.success and result.html:
                        soup = BeautifulSoup(result.html, 'html.parser')

                        if self._is_blocked(soup):
                            logger.info("  ❌ Product page blocked, skipping...")
                            continue

                        # Extract full product info
                        detailed_info = self._extract_complete_product_info(soup, url)
                        detailed_info.update(basic_info)

                        # ✅ Inject cluster_id and query if provided
                        detailed_info["cluster_id"] = basic_info.get("cluster_id", cluster_id)
                        detailed_info["query"] = basic_info.get("query", query)

                        detailed_products.append(detailed_info)
                        logger.info(f"  ✅ Extracted: {detailed_info.get('title', 'Unknown')[:60]}")

                    else:
                        logger.info("  ✗ Failed to load product page")

                except Exception as e:
                    logger.info(f"  ❌ Error: {str(e)}")

                await asyncio.sleep(random.uniform(3, 6))

        logger.info(f"\n🎉 Successfully processed {len(detailed_products)} products")
        unit_price_found = sum(1 for p in detailed_products if p.get('unit_price') or p.get('calculated_unit_price'))
        logger.info(f"🎯 Unit Price Found in: {unit_price_found}/{len(detailed_products)}")

        # ✅ Save to CSV
        if detailed_products:
            flat_data = []
            for product in detailed_products:
                flat_record = {}
                for key, value in product.items():
                    if isinstance(value, (dict, list)):
                        flat_record[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        flat_record[key] = value
                # ✅ Force-add cluster_id and query if not already present
                if cluster_id:
                    flat_record["cluster_id"] = cluster_id
                if query:
                    flat_record["query"] = query

                flat_data.append(flat_record)

            df = pd.DataFrame(flat_data)
            timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_name = f"{self.domain.replace('.', '_')}_{timestamp}.csv"
            s3_key = f"{workspace_id}/{timestamp}/{file_name}"
            full_s3_uri = f"s3://{EXPORT_S3_BUCKET}/{s3_key}"

            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
            csv_buffer.seek(0)

            s3 = boto3.client("s3")
            s3.upload_fileobj(csv_buffer, EXPORT_S3_BUCKET, s3_key)
            logger.info(f"☁️ Uploaded full CSV to S3: {full_s3_uri}")

            # Trigger benchmarking
            run_benchmarking_job(
                workspace_id=workspace_id,
                s3_path=full_s3_uri,
                url=f"https://{self.domain}",
                secret_name=secret_name,
                region_name=region_name,
                benchmarking_row_id=benchmarking_row_id
            )

        return detailed_products



    def _extract_complete_product_info(self, soup, url):
        asin = self._extract_asin_from_url(url)

        basic_info = {
            "url": url,
            "asin": asin,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "domain": self.domain,
            "currency_info": self.currency_info.get(self.domain, {})
        }

        core_details = {
            "title": self._safe_text(soup, "#productTitle") or self._safe_text(soup, "#title"),
            "brand": self._extract_brand(soup),
            "manufacturer": self._extract_manufacturer(soup),
            "model": self._extract_model(soup)
        }

        pricing_info = {
            "current_price": self._extract_current_price(soup),
            "original_price": self._extract_original_price(soup),
            "currency_symbol": self._safe_text(soup, ".a-price-symbol"),
            "savings_amount": self._extract_savings(soup),
            "savings_percentage": self._extract_savings_percentage(soup),
            "deal_price": self._extract_deal_price(soup),
            "subscription_price": self._extract_subscription_price(soup)
        }

        specifications = self._extract_all_specifications(soup)

        measurements = {
            "package_dimensions": self._extract_package_dimensions(soup),
            "item_dimensions": self._extract_item_dimensions(soup),
            "item_weight": self._extract_weight(soup),
            "shipping_weight": self._extract_shipping_weight(soup)
        }

        rating_info = {
            "rating": self._extract_rating_detailed(soup),
            "rating_count": self._extract_rating_count(soup),
            "review_count": self._extract_review_count(soup),
            "rating_breakdown": self._extract_rating_breakdown(soup)
        }

        availability_info = {
            "availability": self._extract_availability(soup),
            "in_stock": self._check_stock_status(soup),
            "delivery_info": self._extract_delivery_info(soup),
            "prime_eligible": bool(soup.select_one(".a-icon-prime")),
            "free_shipping": self._check_free_shipping(soup)
        }

        feature_info = {
            "key_features": self._extract_key_features(soup),
            "bullet_points": self._extract_bullet_points(soup),
            "description": self._extract_description(soup),
            "about_item": self._extract_about_item(soup)
        }

        image_info = {
            "main_image": self._safe_attr(soup, "#landingImage", "src"),
            "gallery_images": self._extract_gallery_images(soup),
            "variant_images": self._extract_variant_images(soup)
        }

        unit_variants = self._extract_unit_variants(soup)
        selected = unit_variants[0] if unit_variants else None
        if selected:
            pricing_info["net_quantity"] = f"{selected['quantity']} count"
            pricing_info["variant_total_price"] = selected["total_price"]
            pricing_info["per_unit_price_display"] = selected["per_unit_price"]

        variant_info = {
            "color_options": self._extract_color_options(soup),
            "size_options": self._extract_size_options(soup),
            "style_options": self._extract_style_options(soup),
            "quantity_options": self._extract_quantity_options(soup),
            "unit_variants": unit_variants or [],
            "unit_variant_count": len(unit_variants) if unit_variants else 0
        }

        additional_info = {
            "best_seller_rank": self._extract_best_seller_rank(soup),
            "category": self._extract_category(soup),
            "date_first_available": self._extract_date_first_available(soup),
            "customer_questions": self._extract_customer_questions_count(soup)
        }

        seller_info = {
            "sold_by": self._extract_seller(soup),
            "shipped_by": self._extract_shipped_by(soup),
            "fulfilled_by": self._extract_fulfilled_by(soup)
        }

        complete_product = {
            **basic_info,
            **core_details,
            **pricing_info,
            **measurements,
            **rating_info,
            **availability_info,
            **feature_info,
            **image_info,
            **variant_info,
            **additional_info,
            **seller_info,
            "unit_price": self._calculate_unit_price(pricing_info),
            "specifications": specifications
        }

        all_variant_data = []
        for variant in unit_variants:
            variant_asin = variant.get("asin")
            if not variant_asin:
                continue
            variant_url = f"https://www.amazon.{self.domain}/dp/{variant_asin}"
            try:
                variant_html = self._fetch_html(variant_url)
                variant_soup = BeautifulSoup(variant_html, "html.parser")
                variant_data = self._extract_complete_product_info(variant_soup, variant_url)
                if variant_data:
                    all_variant_data.append(variant_data)
            except Exception:
                continue

        if all_variant_data:
            complete_product["unit_variants_full"] = all_variant_data

        if not complete_product.get('unit_price') and complete_product.get('current_price'):
            calculated_unit = self._calculate_unit_price(complete_product)
            if calculated_unit:
                complete_product['calculated_unit_price'] = calculated_unit

        return {k: v for k, v in complete_product.items() if v is not None and v != ""}

    def _is_unit_price_text(self, text):
        """Check if text contains unit price information"""
        text_lower = text.lower()
        unit_indicators = [
            'per', 'kg', 'lb', 'oz', 'ml', 'l', 'litre', 'liter', 
            'count', 'piece', 'pack', 'each', 'unit', 'gram', 'pound'
        ]
        return any(indicator in text_lower for indicator in unit_indicators)

    def _extract_variant_counts(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        variants = []
        for button in soup.select(".twisterSwatchWrapper .a-button-text"):
            text = button.get_text(strip=True)
            match = re.search(r'(\d+(?:\.\d+)?)\s*(pcs|pieces|units|count)', text.lower())
            if match:
                qty = float(match.group(1))
                variants.append({"text": text, "quantity": qty, "unit_type": match.group(2)})
        return variants

    def _extract_unit_variants(self, soup):
        variants = []
        for li in soup.select("ul.dimension-values-list li"):
            text = li.get_text(" ", strip=True)
            qty_text = li.select_one(".swatch-title-text-display")
            per_unit = li.select_one(".centralizedApexPricePerUnitCSS span.aok-offscreen")
            total_price = li.select_one(".apex_on_twister_price span.a-price")
            
            if qty_text and per_unit and total_price:
                quantity = float(qty_text.get_text(strip=True))
                per_unit_price = per_unit.get_text(strip=True)
                total_price = total_price.get_text(strip=True)
                variants.append({
                    "quantity": quantity,
                    "per_unit_price": per_unit_price,
                    "total_price": total_price,
                    "text": text
                })
        return variants
    def _normalize_quantity(self, value, unit):
        if unit in ['g', 'gram']:
            return value, 'g'
        elif unit in ['kg']:
            return value * 1000, 'g'
        elif unit in ['oz', 'ounce']:
            return value * 28.3495, 'g'
        elif unit in ['ml']:
            return value, 'ml'
        elif unit in ['litre', 'liter', 'l']:
            return value * 1000, 'ml'
        elif unit in ['pcs', 'pieces', 'count', 'units', 'packs']:
            return value, 'count'
        return value, unit

    def _calculate_unit_price(self, product_info):
        current_price = product_info.get('current_price', '')
        net_quantity = product_info.get('net_quantity', '')

        if not current_price:
            return None

        try:
            price_match = re.search(r'[\d,]+\.?\d*', current_price.replace(',', ''))
            if not price_match:
                return None
            price_value = float(price_match.group().replace(',', ''))
            currency = product_info.get('currency_symbol', '₹')

            match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|kilogram|g|gram|lb|pound|oz|ounce|ml|l|litre|liter|pcs|pieces|count|units|packs?)', net_quantity.lower())
            if not match:
                product_info['unit_price'] = f"{currency}{price_value:.2f}"
                product_info['unit_type'] = 'unknown'
                return product_info['unit_price']

            qty_value = float(match.group(1))
            qty_unit = match.group(2)
            norm_qty_value, norm_qty_unit = self._normalize_quantity(qty_value, qty_unit)

            unit_price_value = price_value / norm_qty_value
            product_info['unit_price'] = f"{currency}{unit_price_value:.2f} per {norm_qty_unit} ({currency}{price_value:.2f} / {int(norm_qty_value)} {norm_qty_unit})"
            product_info['unit_type'] = norm_qty_unit
            return product_info['unit_price']

        except (ValueError, AttributeError):
            return None

    def enforce_unit_price_correction(self, product_info):
        bad_phrases = ['sold by', 'ships from', 'unit count', 'only', 'onsite']
        existing = product_info.get('unit_price', '').lower()
        if not existing or any(bad in existing for bad in bad_phrases):
            return self._calculate_unit_price(product_info)
        return existing

    
    def _extract_all_specifications(self, soup):
        """Extract comprehensive product specifications"""
        specs = {}
        
        # Try different specification table selectors
        spec_tables = soup.select("#productDetails_detailBullets_sections1 tr, #prodDetails tr, .a-keyvalue tr")
        
        for row in spec_tables:
            try:
                key_elem = row.select_one("td:first-child, th, .a-text-bold")
                value_elem = row.select_one("td:last-child, .a-text-normal")
                
                if key_elem and value_elem:
                    key = key_elem.get_text(strip=True).replace(":", "").strip()
                    value = value_elem.get_text(strip=True)
                    
                    if key and value and len(key) < 50:  # Reasonable key length
                        specs[key] = value
            except:
                continue
        
        return specs

    # Additional extraction methods for comprehensive data
    def _extract_brand(self, soup):
        """Extract brand information"""
        brand_selectors = [
            "#bylineInfo", ".a-link-normal#bylineInfo", 
            ".po-brand .po-break-word", "[data-brand]"
        ]
        for selector in brand_selectors:
            brand = self._safe_text(soup, selector)
            if brand:
                # Clean brand text
                brand = brand.replace("Visit the", "").replace("Store", "").strip()
                return brand
        return None

    def _extract_savings_percentage(self, soup):
        """Extract savings percentage"""
        selectors = [".savingsPercentage", ".a-color-price", "[data-testid='savings-percentage']"]
        for selector in selectors:
            savings = self._safe_text(soup, selector)
            if savings and '%' in savings:
                return savings
        return None

    def _extract_package_dimensions(self, soup):
        """Extract package dimensions"""
        specs = soup.select("#productDetails_detailBullets_sections1 tr, #prodDetails tr")
        for row in specs:
            text = row.get_text(strip=True).lower()
            if 'package dimensions' in text or 'product dimensions' in text:
                return row.get_text(strip=True)
        return None

    def _extract_weight(self, soup):
        """Extract item weight"""
        specs = soup.select("#productDetails_detailBullets_sections1 tr, #prodDetails tr")
        for row in specs:
            text = row.get_text(strip=True).lower()
            if any(word in text for word in ['item weight', 'weight', 'shipping weight']):
                return row.get_text(strip=True)
        return None

    def _extract_key_features(self, soup):
        """Extract key product features"""
        features = []
        feature_lists = soup.select("#feature-bullets li, .a-unordered-list li")
        
        for li in feature_lists:
            feature_text = self._safe_text(li, "span")
            if feature_text and len(feature_text) > 20:  # Meaningful features
                features.append(feature_text)
        
        return features[:10]  # Limit to top 10 features

    # Utility methods
    def _extract_asin_from_url(self, url):
        """Extract ASIN from URL"""
        try:
            if '/dp/' in url:
                return url.split('/dp/')[1].split('/')[0].split('?')[0]
        except:
            pass
        return ""

    def _safe_text(self, soup_obj, selector):
        """Safely extract text from element"""
        try:
            element = soup_obj.select_one(selector)
            return element.get_text(strip=True) if element else None
        except:
            return None

    def _safe_attr(self, soup_obj, selector, attribute):
        """Safely extract attribute from element"""
        try:
            element = soup_obj.select_one(selector)
            return element.get(attribute, '').strip() if element else None
        except:
            return None

    # Price extraction methods
    def _extract_current_price(self, soup):
        """Extract current price"""
        selectors = [
            ".a-price .a-offscreen", "#priceblock_ourprice", 
            "#priceblock_dealprice", ".a-price-whole"
        ]
        for selector in selectors:
            price = self._safe_text(soup, selector)
            if price:
                return price
        return None

    def _extract_original_price(self, soup):
        """Extract original price"""
        selectors = [
            ".a-price.a-text-price .a-offscreen", 
            ".priceBlockStrikePriceString", ".a-text-strike"
        ]
        for selector in selectors:
            price = self._safe_text(soup, selector)
            if price:
                return price
        return None

    # Placeholder methods for comprehensive extraction
    def _extract_manufacturer(self, soup): return self._safe_text(soup, ".po-manufacturer .po-break-word")
    def _extract_model(self, soup): return self._safe_text(soup, ".po-model .po-break-word")
    def _extract_savings(self, soup): return self._safe_text(soup, "#youSavePriceDisplayRange")
    def _extract_deal_price(self, soup): return self._safe_text(soup, "#priceblock_dealprice")
    def _extract_subscription_price(self, soup): return self._safe_text(soup, ".a-color-price.sns-price")
    def _extract_item_dimensions(self, soup): return None  # Implement based on specific needs
    def _extract_shipping_weight(self, soup): return None
    def _extract_rating_detailed(self, soup): return self._safe_text(soup, ".a-icon-alt")
    def _extract_rating_count(self, soup): return self._safe_text(soup, "#acrCustomerReviewText")
    def _extract_review_count(self, soup): return None
    def _extract_rating_breakdown(self, soup): return None
    def _extract_availability(self, soup): return self._safe_text(soup, "#availability span")
    def _check_stock_status(self, soup): return None
    def _extract_delivery_info(self, soup): return self._safe_text(soup, "#deliveryBlockMessage")
    def _check_free_shipping(self, soup): return None
    def _extract_bullet_points(self, soup): return None
    def _extract_description(self, soup): return self._safe_text(soup, "#productDescription")
    def _extract_about_item(self, soup): return None
    def _extract_gallery_images(self, soup): return []
    def _extract_variant_images(self, soup): return []
    def _extract_color_options(self, soup): return []
    def _extract_size_options(self, soup): return []
    def _extract_style_options(self, soup): return []
    def _extract_quantity_options(self, soup): return []
    def _extract_best_seller_rank(self, soup): return self._safe_text(soup, "#SalesRank")
    def _extract_category(self, soup): return None
    def _extract_date_first_available(self, soup): return None
    def _extract_customer_questions_count(self, soup): return None
    def _extract_seller(self, soup): return None
    def _extract_shipped_by(self, soup): return None
    def _extract_fulfilled_by(self, soup): return None

    # Search result extraction helpers
    def _extract_price(self, container):
        """Extract price from search result container"""
        selectors = [".a-price .a-offscreen", ".a-price-whole"]
        for selector in selectors:
            price = self._safe_text(container, selector)
            if price:
                return price
        return None

    def _extract_image(self, container):
        """Extract image from search result"""
        img = self._safe_attr(container, ".s-image", "src")
        return img if img and img.startswith('http') else None

    def _extract_rating(self, container):
        """Extract rating from search result"""
        return self._safe_text(container, ".a-icon-alt")

# Main execution function
async def comprehensive_product_analysis(
    search_query,
    workspace_id,
    domain="amazon.in",
    num_pages=2,
    secret_name=None,
    region_name=None,
    benchmarking_row_id=None,
    cluster_id=None
):
    """
    Complete comprehensive product analysis with unit price focus
    """
    scraper = ComprehensiveScraper(domain)

    logger.info("=" * 80)
    logger.info("🎯 COMPREHENSIVE AMAZON PRODUCT ANALYZER")
    logger.info("🔍 PRIMARY FOCUS: UNIT PRICE EXTRACTION")
    logger.info("=" * 80)

    # Step 1: Search for products
    search_results = await scraper.search_products(search_query, num_pages)

    if not search_results:
        logger.error("❌ No products found!")
        return []

    # Step 2: Get comprehensive details
    detailed_products = await scraper.get_comprehensive_product_details(
        product_urls=search_results,
        workspace_id=workspace_id,
        secret_name=secret_name,
        region_name=region_name,
        benchmarking_row_id=benchmarking_row_id,
        cluster_id=cluster_id
    )

    return detailed_products


    
async def main(queries, domain, pages=3):
    logger(f"🚀 Starting Comprehensive Product Analysis")

    domain_map = {
        "amazon_uae": "amazon.ae",
        "amazon_in": "amazon.in",
        "amazon_jpn": "amazon.co.jp",
        "amazon_sa": "amazon.sa"
    }
    actual_domain = domain_map.get(domain, domain)
    logger.info(f"🌐 Resolved Domain: {actual_domain}")

    filtered_queries = [q.strip() for q in queries if q and q.strip()]
    if not filtered_queries:
        logger.error("❌ All queries were empty or invalid. Exiting.")
        return

    all_results = []

    for query in filtered_queries:
        logger.info(f"\n🔍 Running query: {query}")
        try:
            products = await comprehensive_product_analysis(
                search_query=query,
                domain=actual_domain,
                num_pages=1,
                workspace_id=workspace_id,
                secret_name=secret_name,
                region_name=region_name,
                benchmarking_row_id=benchmarking_row_id,
                cluster_id=cluster_id
            )
            # products = await comprehensive_product_analysis(query, actual_domain, pages)
        except Exception as e:
            logger.error(f"❌ Error while processing '{query}': {str(e)}")
            continue

        if products:
            logger.info(f"✅ Found {len(products)} products for '{query}'")
            all_results.extend(products)
        else:
            logger(f"⚠️ No products found for '{query}'")

    if all_results:
        df = pd.DataFrame(all_results)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_domain = actual_domain.replace('.', '_')
        filename = f"comprehensive_summary_{safe_domain}_{timestamp}.csv"

        # Save locally
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        logger.info(f"\n💾 Comprehensive summary saved locally to: {filename}")
        logger.info(f"📦 Total Products: {len(df)}")