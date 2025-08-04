from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# --- Product Data Schema ---
class ProductSchema(BaseModel):
    title: Optional[str] = Field(None, description="Title of the product")
    price: Optional[float] = Field(None, description="Price of the product")
    currency: Optional[str] = Field(None, description="Currency of the product price")
    url: Optional[str] = Field(None, description="URL of the product page")
    image_url: Optional[str] = Field(None, description="URL of the product image")
    shop_name: Optional[str] = Field(None, description="Shop or merchant name")
    website: str = Field(..., description="Website where the product was scraped from")
    query: str = Field(..., description="Original search query used")
    cluster_id: str = Field(..., description="Cluster ID associated with the query")
    scraped_at: datetime = Field(..., description="Timestamp of when the data was scraped")


# --- Sample HTML for Rakuten (for schema testing/generation) ---
RAKUTEN_SAMPLE_HTML = """
<div class="dui-card searchresultitem">
  <h2 class="title--2KRhr">
    <a href="https://item.rakuten.co.jp/sample-laptop" class="title-link--3Yuev">Sample Laptop Title</a>
  </h2>
  <img src="https://image.rakuten.co.jp/sample-laptop.jpg" class="image--x5mNi" />
  <div class="price--3zUvK">¥99,800</div>
  <div class="content merchant">
    <a href="https://shop.rakuten.co.jp/sample-shop">Sample Shop Name</a>
  </div>
</div>
"""
AMAZON_SAMPLE_HTML = """
<div class="sg-col-inner">
  <div class="s-widget-container s-spacing-small s-widget-container-height-small celwidget">
    <div class="puis-card-container s-card-container">
      <div class="a-section a-spacing-base">   
        <!-- Product Image -->
        <div class="s-product-image-container aok-relative s-text-center">
          <span data-component-type="s-product-image">
            <a class="a-link-normal s-no-outline" href="/-/en/Itoen-Labelless-Green-Bottles-Hojicha/dp/B0CQ4FHGL8">
              <div class="a-section aok-relative s-image-square-aspect">
                <img class="s-image" src="https://m.media-amazon.com/images/I/61JBIK8y1EL._AC_UL320_.jpg" alt="Itoen Labelless Oi Tea Green Tea" />
              </div>
            </a>
          </span>
        </div>
        <!-- Title -->
        <div class="a-section a-spacing-small">
          <div data-cy="title-recipe">
            <a class="a-link-normal s-line-clamp-4 s-link-style a-text-normal" href="/-/en/Itoen-Labelless-Green-Bottles-Hojicha/dp/B0CQ4FHGL8">
              <h2 class="a-size-base-plus a-spacing-none a-color-base a-text-normal">
                <span>Itoen Labelless Oi Tea Green Tea 9.5 fl oz (280 ml) x 24 Bottles + Itoen Oi Ocha Hojicha 9.5 fl oz (280 ml) x 24 Bottles</span>
              </h2>
            </a>
          </div>
        </div>
        <!-- Price -->
        <div data-cy="secondary-offer-recipe" class="a-section a-spacing-none a-spacing-top-mini">
          <span class="a-color-price">¥4,019</span>
        </div>
      </div>
    </div>
  </div>
</div>
"""

AMAZON_UAE_SAMPLE_HTML="""
<div class="sg-col-inner">
  <div class="s-widget-container s-spacing-small s-widget-container-height-small celwidget">
    <div class="puis-card-container s-card-container">
      <div class="a-section a-spacing-base">   
        <!-- Product Image -->
        <div class="s-product-image-container aok-relative s-text-center">
          <span data-component-type="s-product-image">
            <a class="a-link-normal s-no-outline" href="/ITO-EN-Unsweetened-Green-500ml/dp/B0857XYYFW">
              <div class="a-section aok-relative s-image-square-aspect">
                <img class="s-image" src="https://m.media-amazon.com/images/I/71kxZxo2zUS._AC_UL320_.jpg" alt="ITO EN Unsweetened Green Tea, 500ml" />
              </div>
            </a>
          </span>
        </div>
        <!-- Title -->
        <div class="a-section a-spacing-small">
          <div data-cy="title-recipe">
            <a class="a-link-normal s-line-clamp-4 s-link-style a-text-normal" href="/ITO-EN-Unsweetened-Green-500ml/dp/B0857XYYFW">
              <h2 class="a-size-base-plus a-spacing-none a-color-base a-text-normal">
                <span>Unsweetened Green Tea, 500ml</span>
              </h2>
            </a>
          </div>
        </div>
        <!-- Price -->
        <div data-cy="price-recipe" class="a-section a-spacing-none a-spacing-top-mini">
          <span class="a-color-price">AED 6.22</span>
        </div>
      </div>
    </div>
  </div>
</div>
"""
ALIBABA_SAMPLE_HTML = """
<div class="fy23-search-card m-gallery-product-item-v2">
  <div class="search-card-m-imgarea">
    <a href="https://www.alibaba.com/product-detail/sample-battery-pack" class="search-card-e-slider__link">
      <img src="https://s.alicdn.com/sample-battery.jpg" class="search-card-e-slider__img">
    </a>
  </div>
  <div class="card-info">
    <h2 class="search-card-e-title">
      <a href="https://www.alibaba.com/product-detail/sample-battery-pack" target="_blank">
        <span>Sample 3V Lithium Battery Pack</span>
      </a>
    </h2>
    <div class="search-card-e-price-main">$1.50</div>
    <div class="search-card-m-sale-features__item">Min. order: 10 pieces</div>
    <a href="https://szkingkong.en.alibaba.com" class="search-card-e-company">Sample Supplier Co., Ltd.</a>
  </div>
</div>
"""
MADE_IN_CHINA_SAMPLE_HTML = """
<div class="prod-content">
  <div class="prod-info">
    <!-- Product Title -->
    <h2 class="product-name">
      <a href="//vitekfactory.en.made-in-china.com/product/pAyUOJBKniVc/China-Low-Price-Lightweight-Laptop.html"
         title="Low Price Lightweight Laptop"
         target="_blank">
        Low Price Lightweight <strong>Laptop</strong> 15.6 Inch Business Laptop
      </a>
    </h2>

    <!-- Product Price -->
    <div class="product-property">
      <div class="info price-info">
        <strong class="price">US $ 115.0-153.0</strong>
        <span class="price_hint">(FOB Price)</span>
      </div>
      <div class="info">1 Piece<span class="price_hint">(MOQ)</span></div>
    </div>

    <!-- Product Specs -->
    <div class="extra-property cf">
      <ul class="property-list">
        <li class="J-faketitle ellipsis">Screen Size: <span class="property-val">15.6 Inch</span></li>
        <li class="J-faketitle ellipsis">Operating System: <span class="property-val">Windows</span></li>
        <li class="J-faketitle ellipsis">Weight: <span class="property-val">1.5~2.0 kg</span></li>
        <li class="J-faketitle ellipsis">Processor Type: <span class="property-val">N5095/ N95</span></li>
        <li class="J-faketitle ellipsis">RAM Capacity: <span class="property-val">8GB/16GB/32GB</span></li>
        <li class="J-faketitle ellipsis">Hard Disk Capacity: <span class="property-val">128/256/512GB/1000GB</span></li>
      </ul>
    </div>

    <!-- Company Name -->
    <div class="company-info">
      <a href="//vitekfactory.en.made-in-china.com" class="compnay-name">
        <span>Shenzhen Vitek Electronics Co., Ltd.</span>
      </a>
    </div>
  </div>
</div>
"""
AMAZON_SA_SAMPLE_HTML = """
<div data-asin="B09XYZ1234" data-component-type="s-search-result" class="sg-col-inner">
  <div class="s-widget-container s-spacing-small s-widget-container-height-small celwidget">
    <div class="puis-card-container s-card-container">
      <div class="a-section a-spacing-base">

        <!-- Sponsored Label -->
        <span class="puis-label-Sponsored">
          <span class="puis-sponsored-label-text">Sponsored</span>
        </span>

        <!-- Product Image -->
        <div class="s-product-image-container aok-relative s-text-center">
          <span data-component-type="s-product-image">
            <a class="a-link-normal s-no-outline" href="/Some-Product-Title/dp/B09XYZ1234">
              <div class="a-section aok-relative s-image-square-aspect">
                <img class="s-image" src="https://m.media-amazon.com/images/I/71exampleimage.jpg" alt="Sample Product Image" />
              </div>
            </a>
          </span>
        </div>

        <!-- Title -->
        <div class="a-section a-spacing-small">
          <div data-cy="title-recipe">
            <a class="a-link-normal s-line-clamp-4 s-link-style a-text-normal" href="/Some-Product-Title/dp/B09XYZ1234">
              <h2 class="a-size-base-plus a-spacing-none a-color-base a-text-normal">
                <span>Sample Product Title for Amazon.sa</span>
              </h2>
            </a>
          </div>
        </div>

        <!-- Price -->
        <div class="a-section a-spacing-none a-spacing-top-mini">
          <span class="a-price">
            <span class="a-offscreen">SAR 99.00</span>
          </span>
        </div>

        <!-- Rating -->
        <div class="a-row a-size-small">
          <span aria-label="4.3 out of 5 stars">
            <span class="a-icon-alt">4.3 out of 5 stars</span>
          </span>
        </div>

        <!-- Reviews Count -->
        <div class="a-row a-size-small">
          <span class="a-size-base s-underline-text">1,234</span>
        </div>

      </div>
    </div>
  </div>
</div>
"""

# --- Website CSS Selectors for scraping ---
website_css: Dict[str, Any] = {
    "rakuten": {
        "baseSelector": "div.dui-card.searchresultitem",
        "fields": [
            {
                "name": "title",
                "selector": "a.title-link--3Yuev",
                "type": "text",
            },
            {
                "name": "url",
                "selector": "a.title-link--3Yuev",
                "type": "attribute",
                "attribute": "href"
            },
            {
                "name": "image_url",
                "selector": "img.image--x5mNi",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "price",
                "selector": "div.price--3zUvK",
                "type": "text"
            }
        ]
    },
    # Keeping these for future scraping configs
    "amazon_jpn": {
    "baseSelector": "div.s-widget-container.celwidget",
    "fields": [
        {
            "name": "title",
            "selector": "a.a-text-normal",
            "type": "text"
        },
        {
            "name": "url",
            "selector": "a.a-link-normal",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "image_url",
            "selector": "img.s-image",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "price",
            "selector": "span.a-price-whole",
            "type": "text"
        }
    ]
},
    "alibaba": {
    "baseSelector": "div.fy23-search-card.m-gallery-product-item-v2",
    "fields": [
        {
            "name": "title",
            "selector": "a.a-text-normal",
            "type": "text"
        },
        {
            "name": "url",
            "selector": "a.search-card-e-slider__link",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "image_url",
            "selector": "img.search-card-e-slider__img",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "price",
            "selector": "div.search-card-e-price-main",
            "type": "text"
        }
    ]
},
    "amazon_uae": {
    "baseSelector": "div.s-widget-container.celwidget",
    "fields": [
        {
            "name": "title",
            "selector": "a.a-text-normal",
            "type": "text"
        },
        {
            "name": "url",
            "selector": "a.a-link-normal",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "image_url",
            "selector": "img.s-image",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "price",
            "selector": "span.a-price",
            "type": "text"
    }
    ]
},
    "made_in_china": {
    "baseSelector": "div.prod-content",
    "fields": [
        {
            "name": "title",
            "selector": "h2.product-name a",
            "type": "text"
        },
        {
            "name": "url",
            "selector": "h2.product-name a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "image_url",
            "selector": "div.prod-content img",
            "type": "attribute",
            "attribute": "src"
        },
        {
            "name": "price",
            "selector": "div.price-info strong.price",
            "type": "text"
        },
        {
            "name": "company_name",
            "selector": "div.company-info a span",
            "type": "text"
        }
    ]
},
    "amazon_sa": {
        "baseSelector": 'div[data-asin][data-component-type="s-search-result"]',
        "fields": [
            {
                "name": "title",
                "selector": "h2 span",
                "type": "text"
            },
            {
                "name": "url",
                "selector": "h2 a.a-link-normal",
                "type": "attribute",
                "attribute": "href"
            },
            {
                "name": "image_url",
                "selector": "img.s-image",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "price",
                "selector": "span.a-price span.a-offscreen",
                "type": "text"
            }
        ]
    }
}


# --- Website Scraper Configuration ---
website_configs: Dict[str, Dict[str, Any]] = {
    "rakuten": {
        "base_url_template": "https://search.rakuten.co.jp/search/mall/{encoded_keyword}/?p={page_num}",
        "extraction_css_selector": website_css["rakuten"]["baseSelector"],
        "product_schema": website_css["rakuten"]["fields"],
        "sample_html": RAKUTEN_SAMPLE_HTML,
    },
    "amazon_jpn":{
        "base_url_template": "https://www.amazon.co.jp/s?k={encoded_keyword}&page={page_num}",
        "extraction_css_selector": website_css["amazon_jpn"]["baseSelector"],
        "product_schema": website_css["amazon_jpn"]["fields"],
        "sample_html": AMAZON_SAMPLE_HTML,
    },
    "alibaba": {
        "base_url_template": "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={encoded_keyword}&page={page_num}",
        "extraction_css_selector": website_css["alibaba"]["baseSelector"],
        "product_schema": website_css["alibaba"]["fields"],
        "sample_html": ALIBABA_SAMPLE_HTML,
    },
    "amazon_uae": {
        "base_url_template": "https://www.amazon.ae/s?k={encoded_keyword}&page={page_num}",
        "extraction_css_selector": website_css["amazon_uae"]["baseSelector"],
        "product_schema": website_css["amazon_uae"]["fields"],
        "sample_html": AMAZON_UAE_SAMPLE_HTML,
    },
    "made_in_china": {
    "base_url_template": (
        "https://www.made-in-china.com/productdirectory.do?"
        "word={encoded_keyword}&subaction=hunt&style=b&mode=and&code=0"
        "&comProvince=nolimit&order=0&isOpenCorrection=1&log_from=4&page={page_num}"
    ),
    "extraction_css_selector": website_css["made_in_china"]["baseSelector"],
    "product_schema": website_css["made_in_china"]["fields"],
    "sample_html": MADE_IN_CHINA_SAMPLE_HTML,
},
    "amazon_sa": {
    "base_url_template": "https://www.amazon.sa/s?k={encoded_keyword}&page={page_num}",
    "extraction_css_selector": website_css["amazon_sa"]["baseSelector"],
    "product_schema": website_css["amazon_sa"]["fields"],
    "sample_html": AMAZON_SA_SAMPLE_HTML,
}
}   

# --- Snowflake Configuration ---
SNOWFLAKE_SCHEMA_NAME: str = "default_schema_placeholder"
SNOWFLAKE_TABLE_NAME: str = "NORMALISED_DATA"

# --- Currency Symbols to ISO 4217 codes mapping ---
CURRENCY_SYMBOLS_MAP: Dict[str, str] = {
    '円': 'JPY',
    '€': 'EUR',
    '$': 'USD',
    'AED': 'AED',
    'AED': 'AED',
    'SAR': 'SAR',
    'OMR': 'OMR',
    'BHD': 'BHD',
    'KWD': 'KWD',
    'QAR': 'QAR'
}
