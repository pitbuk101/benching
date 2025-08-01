--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

-- Started on 2025-04-02 18:55:50 IST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 16450)
-- Name: :tenant_id; Type: SCHEMA; Schema: -; Owner: :tenant_id
--

CREATE ROLE ":tenant_id" WITH LOGIN;

ALTER ROLE ":tenant_id" WITH PASSWORD ':password';

CREATE SCHEMA ":tenant_id";

ALTER SCHEMA ":tenant_id" OWNER TO ":tenant_id";


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 229 (class 1259 OID 16451)
-- Name: alembic_version; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE ":tenant_id".alembic_version OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16454)
-- Name: analytics_idea_details; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".analytics_idea_details (
    category_name text NOT NULL,
    analytics_name text NOT NULL,
    opportunity_query_id integer,
    opportunity_insight text,
    impact text,
    linked_insight jsonb,
    analytics_ideas jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".analytics_idea_details OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16460)
-- Name: top_idea_details; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".top_idea_details (
    category_name text NOT NULL,
    file_timestamp text NOT NULL,
    idea_number integer NOT NULL,
    idea text,
    analytics_name text,
    impact text,
    linked_insight jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".top_idea_details OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16466)
-- Name: top_ideas_knowledge_base; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".top_ideas_knowledge_base (
    category_name text NOT NULL,
    analytics_name text NOT NULL,
    opportunity_query_id integer,
    expert_inputs jsonb
);


ALTER TABLE ":tenant_id".top_ideas_knowledge_base OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16471)
-- Name: analytics_ideas_opportunities_view; Type: VIEW; Schema: :tenant_id; Owner: postgres
--

CREATE VIEW ":tenant_id".analytics_ideas_opportunities_view AS
 SELECT ti.category_name,
    ti.file_timestamp,
    ti.idea_number,
    ti.idea,
    ti.analytics_name,
    ti.impact,
    ti.linked_insight,
    ti.updated_ts,
    aid.opportunity_insight,
    tikb.expert_inputs
   FROM ((( SELECT top_idea_details.category_name,
            top_idea_details.file_timestamp,
            top_idea_details.idea_number,
            top_idea_details.idea,
            top_idea_details.analytics_name,
            top_idea_details.impact,
            top_idea_details.linked_insight,
            top_idea_details.updated_ts
           FROM ":tenant_id".top_idea_details
          WHERE (top_idea_details.file_timestamp = ( SELECT max(top_idea_details_1.file_timestamp) AS max
                   FROM ":tenant_id".top_idea_details top_idea_details_1))) ti
     LEFT JOIN ":tenant_id".top_ideas_knowledge_base tikb ON (((ti.analytics_name = tikb.analytics_name) AND (ti.category_name = tikb.category_name))))
     LEFT JOIN ":tenant_id".analytics_idea_details aid ON (((ti.analytics_name = aid.analytics_name) AND (ti.category_name = aid.category_name))));


ALTER VIEW ":tenant_id".analytics_ideas_opportunities_view OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16476)
-- Name: categories; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".categories (
    id character varying(10),
    name character varying(100)
);


ALTER TABLE ":tenant_id".categories OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16479)
-- Name: categories_news_data; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".categories_news_data (
    news_id character varying(255) NOT NULL,
    source_id character varying(500),
    information_source character varying(500),
    source_rank character varying(500),
    image_url character varying(3000),
    keyword_type_id character varying(500),
    keyword_names character varying(500),
    category_id character varying(255),
    category_name character varying(255),
    keyword_type character varying(500),
    description text,
    title character varying(3000),
    url character varying(3000),
    news_type character varying(100),
    publication_date timestamp with time zone
);


ALTER TABLE ":tenant_id".categories_news_data OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16484)
-- Name: category_news; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".category_news (
    news_id text NOT NULL,
    category_name text,
    issue_in_webpage_loading text,
    is_relative text,
    news_content text,
    bullet_points_summary jsonb
);


ALTER TABLE ":tenant_id".category_news OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16489)
-- Name: news; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".news (
    news_id text NOT NULL,
    title text,
    description text,
    url text,
    image_url text,
    information_source text,
    last_modified_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    publication_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".news OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 16496)
-- Name: category_news_view; Type: VIEW; Schema: :tenant_id; Owner: postgres
--

CREATE VIEW ":tenant_id".category_news_view AS
 SELECT category_news.news_id,
    category_news.category_name,
    category_news.news_content,
    category_news.bullet_points_summary,
    news.title,
    news.description,
    news.url,
    news.image_url,
    news.publication_date
   FROM (":tenant_id".category_news
     JOIN ":tenant_id".news ON ((news.news_id = category_news.news_id)))
  WHERE (category_news.is_relative = 'Y'::text);


ALTER VIEW ":tenant_id".category_news_view OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16500)
-- Name: category_qna; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".category_qna (
    category_name text NOT NULL,
    qna jsonb
);


ALTER TABLE ":tenant_id".category_qna OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 16505)
-- Name: category_qna_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".category_qna_final (
    category_name text NOT NULL,
    qna jsonb
);


ALTER TABLE ":tenant_id".category_qna_final OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16510)
-- Name: chat_history; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".chat_history (
    chat_id text NOT NULL,
    recommended_rca jsonb,
    recommended_ideas jsonb,
    chat_message_history jsonb
);


ALTER TABLE ":tenant_id".chat_history OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 16515)
-- Name: chat_history_new; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".chat_history_new (
    chat_id integer NOT NULL,
    recommended_rca jsonb,
    recommended_ideas jsonb,
    chat_message_history jsonb
);


ALTER TABLE ":tenant_id".chat_history_new OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16520)
-- Name: chat_id_sequence; Type: SEQUENCE; Schema: :tenant_id; Owner: postgres
--

CREATE SEQUENCE ":tenant_id".chat_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE ":tenant_id".chat_id_sequence OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 16521)
-- Name: common_chat_history; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".common_chat_history (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    model_used text,
    request text,
    response text,
    created_time jsonb
);


ALTER TABLE ":tenant_id".common_chat_history OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 16526)
-- Name: contract_details; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".contract_details (
    document_id integer NOT NULL,
    region text,
    supplier text,
    sku text,
    entity_extraction jsonb,
    benchmarking jsonb,
    clauses jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".contract_details OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 16532)
-- Name: contract_sku_details; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".contract_sku_details (
    document_id integer NOT NULL,
    sku_id text NOT NULL,
    original_code text,
    description text NOT NULL,
    price double precision NOT NULL,
    price_type text,
    currency text,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".contract_sku_details OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 16538)
-- Name: curated_news_insights; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".curated_news_insights (
    created_date timestamp with time zone,
    created_at integer NOT NULL,
    category_id character varying(100),
    title character varying(3000) NOT NULL,
    content text,
    topic_name character varying(500) NOT NULL,
    topic_id integer,
    related_news jsonb,
    category_name character varying(200),
    id integer NOT NULL
);


ALTER TABLE ":tenant_id".curated_news_insights OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 16543)
-- Name: curated_news_insights_id_seq; Type: SEQUENCE; Schema: :tenant_id; Owner: postgres
--

CREATE SEQUENCE ":tenant_id".curated_news_insights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE ":tenant_id".curated_news_insights_id_seq OWNER TO postgres;

--
-- TOC entry 4653 (class 0 OID 0)
-- Dependencies: 248
-- Name: curated_news_insights_id_seq; Type: SEQUENCE OWNED BY; Schema: :tenant_id; Owner: postgres
--

ALTER SEQUENCE ":tenant_id".curated_news_insights_id_seq OWNED BY ":tenant_id".curated_news_insights.id;


--
-- TOC entry 249 (class 1259 OID 16544)
-- Name: dashboard_reporting; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".dashboard_reporting (
    category_name text NOT NULL,
    report_id text NOT NULL,
    report_name text,
    sub_report_name text NOT NULL,
    title text,
    description text
);


ALTER TABLE ":tenant_id".dashboard_reporting OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 16549)
-- Name: dashboard_reporting_dummy2; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".dashboard_reporting_dummy2 (
    category_name text NOT NULL,
    report_id text NOT NULL,
    report_name text,
    sub_report_name text NOT NULL,
    title text,
    description text
);


ALTER TABLE ":tenant_id".dashboard_reporting_dummy2 OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 16554)
-- Name: dax_entity_lookup; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".dax_entity_lookup (
    entity_name text NOT NULL,
    value_range text NOT NULL,
    entity_values jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".dax_entity_lookup OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 16560)
-- Name: dax_entity_lookup_dummy2; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".dax_entity_lookup_dummy2 (
    entity_name text NOT NULL,
    value_range text,
    entity_values jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".dax_entity_lookup_dummy2 OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 16566)
-- Name: demo_category_qna; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".demo_category_qna (
    category_name text NOT NULL,
    qna jsonb
);


ALTER TABLE ":tenant_id".demo_category_qna OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 16571)
-- Name: document_info; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".document_info (
    document_id integer NOT NULL,
    document_type text,
    region text,
    category text,
    supplier text,
    sku text,
    content text,
    summary text,
    entity_extraction jsonb,
    benchmarking jsonb,
    clauses jsonb,
    document_filename text,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".document_info OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 16577)
-- Name: features; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".features (
    feature_name text NOT NULL,
    status boolean,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".features OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 16583)
-- Name: idea_generation_context; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".idea_generation_context (
    insight_id integer NOT NULL,
    linked_insight jsonb,
    sku_qna text,
    supplier_qna text,
    sku_360 text,
    supplier_360 text,
    category_qna text,
    definitions text,
    recommended_ideas jsonb,
    recommended_rca jsonb,
    category_name text,
    alert_type integer NOT NULL,
    alert_name text NOT NULL,
    parameter text,
    impact text,
    label text,
    updated_at timestamp without time zone,
    rule_id integer,
    created_year_month integer
);


ALTER TABLE ":tenant_id".idea_generation_context OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 16588)
-- Name: idea_generation_context_dummy; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".idea_generation_context_dummy (
    insight_id integer NOT NULL,
    linked_insight jsonb,
    sku_qna text,
    supplier_qna text,
    sku_360 text,
    supplier_360 text,
    category_qna text,
    definitions text,
    recommended_ideas jsonb,
    recommended_rca jsonb,
    category_name text,
    alert_type integer NOT NULL,
    alert_name text NOT NULL,
    parameter text,
    impact text,
    label text,
    updated_at timestamp without time zone,
    rule_id integer
);


ALTER TABLE ":tenant_id".idea_generation_context_dummy OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 16593)
-- Name: idea_generation_context_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".idea_generation_context_final (
    insight_id integer NOT NULL,
    linked_insight jsonb,
    sku_qna text,
    supplier_qna text,
    sku_360 text,
    supplier_360 text,
    category_qna text,
    definitions text,
    recommended_ideas jsonb,
    recommended_rca jsonb,
    category_name text,
    alert_type integer NOT NULL,
    alert_name text NOT NULL,
    parameter text,
    impact text,
    label text
);


ALTER TABLE ":tenant_id".idea_generation_context_final OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 16598)
-- Name: insights_master; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".insights_master (
    insight_id integer NOT NULL,
    alert_type integer NOT NULL,
    alert_name text NOT NULL,
    parameter text,
    label text,
    linked_insight text,
    sku text,
    supplier text,
    created_time text NOT NULL,
    impact text,
    document_id integer,
    category_name text,
    objectives text,
    updated_at timestamp without time zone,
    rule_id integer,
    created_year_month integer
);


ALTER TABLE ":tenant_id".insights_master OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 16603)
-- Name: insights_master_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".insights_master_final (
    insight_id integer NOT NULL,
    alert_type integer NOT NULL,
    alert_name text NOT NULL,
    parameter text,
    label text,
    linked_insight text,
    sku text,
    supplier text,
    created_time text NOT NULL,
    impact text,
    document_id integer,
    category_name text,
    objectives text
);


ALTER TABLE ":tenant_id".insights_master_final OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 16608)
-- Name: key_facts_config; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".key_facts_config (
    category_name text NOT NULL,
    config_name text NOT NULL,
    config jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".key_facts_config OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 16614)
-- Name: key_facts_config_dummy2; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".key_facts_config_dummy2 (
    category_name text NOT NULL,
    config_name text NOT NULL,
    config jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".key_facts_config_dummy2 OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 16620)
-- Name: keywords_news_data; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".keywords_news_data (
    news_id character varying(255) NOT NULL,
    source_id character varying(500),
    information_source character varying(500),
    source_rank character varying(500),
    image_url character varying(3000),
    keyword_type_id character varying(500),
    keyword_names character varying(500),
    category_id character varying(255),
    category_name character varying(255),
    keyword_type character varying(500),
    description text,
    title character varying(3000),
    url character varying(3000),
    news_type character varying(100),
    publication_date timestamp with time zone
);


ALTER TABLE ":tenant_id".keywords_news_data OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 16625)
-- Name: market_approach_strategy_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".market_approach_strategy_final (
    market_approach text NOT NULL,
    is_auctionable boolean,
    incumbency integer DEFAULT 0,
    category_positioning jsonb,
    supplier_relationship jsonb
);


ALTER TABLE ":tenant_id".market_approach_strategy_final OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 16631)
-- Name: negotiation_chat_history; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_chat_history (
    negotiation_id text NOT NULL,
    chat_message_history jsonb
);


ALTER TABLE ":tenant_id".negotiation_chat_history OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 16636)
-- Name: negotiation_details; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_details (
    negotiation_id text NOT NULL,
    supplier_name text,
    generated_arguments jsonb,
    generated_counter_arguments jsonb,
    generated_rebuttals jsonb,
    generated_emails jsonb
);


ALTER TABLE ":tenant_id".negotiation_details OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 16641)
-- Name: negotiation_insights; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_insights (
    insight_id integer NOT NULL,
    supplier_id text,
    supplier_name text,
    category_name text,
    label text,
    objective text,
    reinforcements jsonb,
    minimum_spend_threshold double precision,
    analytics_name text
);


ALTER TABLE ":tenant_id".negotiation_insights OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 16646)
-- Name: negotiation_insights_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_insights_final (
    insight_id integer NOT NULL,
    supplier_id text,
    supplier_name text,
    category_name text,
    label text,
    objective text,
    reinforcements jsonb,
    minimum_spend_threshold double precision
);


ALTER TABLE ":tenant_id".negotiation_insights_final OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 16651)
-- Name: negotiation_objective; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_objective (
    supplier_id text NOT NULL,
    supplier_name text,
    category_name text NOT NULL,
    objective text NOT NULL,
    objective_summary text,
    analytics_names text[] DEFAULT ARRAY[]::text[]
);


ALTER TABLE ":tenant_id".negotiation_objective OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 16657)
-- Name: negotiation_objective_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_objective_final (
    supplier_id text NOT NULL,
    supplier_name text,
    category_name text NOT NULL,
    objective text NOT NULL,
    objective_summary text
);


ALTER TABLE ":tenant_id".negotiation_objective_final OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 16662)
-- Name: negotiation_references_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_references_final (
    l1_objective text,
    l1_objective_description text,
    samples jsonb,
    sample_emails jsonb
);


ALTER TABLE ":tenant_id".negotiation_references_final OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 16667)
-- Name: negotiation_relationship_details_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_relationship_details_final (
    relationship text NOT NULL,
    expert_input text,
    general_information text,
    argument_strategy text,
    negotiation_strategy text
);


ALTER TABLE ":tenant_id".negotiation_relationship_details_final OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 16672)
-- Name: negotiation_strategy_details_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_strategy_details_final (
    category_name text NOT NULL,
    pricing_methodology jsonb,
    contract_methodology jsonb,
    is_auctionable boolean,
    supplier_market_complexity text,
    business_relevance text,
    category_positioning text
);


ALTER TABLE ":tenant_id".negotiation_strategy_details_final OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 16677)
-- Name: negotiation_strategy_tones_n_tactics; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".negotiation_strategy_tones_n_tactics (
    tone_name text NOT NULL,
    tone_desciption text,
    supplier_positioning text NOT NULL,
    buyer_attractiveness text,
    tactics jsonb
);


ALTER TABLE ":tenant_id".negotiation_strategy_tones_n_tactics OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 16682)
-- Name: suppliers_news_data; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".suppliers_news_data (
    tools_supplier_id character varying(500),
    tools_supplier_name character varying(255),
    supplier_id character varying(500),
    parent_supplier_name character varying(1000),
    category_id character varying(255),
    channel character varying(500),
    count character varying(255),
    image_url character varying(3000),
    industry_name character varying(500),
    news_id character varying(255) NOT NULL,
    title character varying(3000),
    language_name character varying(255),
    publication_date timestamp with time zone,
    source_id character varying(255),
    information_source character varying(500),
    source_rank character varying(255),
    description text,
    supplier_name character varying(1000),
    topic_name character varying(255),
    url character varying(3000),
    news_type character varying(100),
    company_id character varying(255),
    category_name character varying(200)
);


ALTER TABLE ":tenant_id".suppliers_news_data OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 16687)
-- Name: news_aggregations; Type: VIEW; Schema: :tenant_id; Owner: postgres
--

CREATE VIEW ":tenant_id".news_aggregations AS
 SELECT categories_news_data.news_id,
    categories_news_data.source_id,
    categories_news_data.information_source,
    categories_news_data.source_rank,
    categories_news_data.category_id,
    categories_news_data.category_name,
    categories_news_data.description,
    categories_news_data.title,
    categories_news_data.publication_date,
    categories_news_data.news_type,
    categories_news_data.category_name AS entity_name
   FROM ":tenant_id".categories_news_data
  WHERE (categories_news_data.publication_date > (CURRENT_DATE - '6 days'::interval))
UNION ALL
 SELECT keywords_news_data.news_id,
    keywords_news_data.source_id,
    keywords_news_data.information_source,
    keywords_news_data.source_rank,
    keywords_news_data.category_id,
    keywords_news_data.category_name,
    keywords_news_data.description,
    keywords_news_data.title,
    keywords_news_data.publication_date,
    keywords_news_data.news_type,
    keywords_news_data.keyword_type AS entity_name
   FROM ":tenant_id".keywords_news_data
  WHERE (keywords_news_data.publication_date > (CURRENT_DATE - '6 days'::interval))
UNION ALL
 SELECT suppliers_news_data.news_id,
    suppliers_news_data.source_id,
    suppliers_news_data.information_source,
    suppliers_news_data.source_rank,
    suppliers_news_data.category_id,
    suppliers_news_data.category_name,
    suppliers_news_data.description,
    suppliers_news_data.title,
    suppliers_news_data.publication_date,
    suppliers_news_data.news_type,
    suppliers_news_data.supplier_name AS entity_name
   FROM ":tenant_id".suppliers_news_data
  WHERE (suppliers_news_data.publication_date > (CURRENT_DATE - '6 days'::interval));


ALTER VIEW ":tenant_id".news_aggregations OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 16692)
-- Name: news_feed_status; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".news_feed_status (
    status character varying(30),
    date_run timestamp with time zone,
    date_run_int integer
);


ALTER TABLE ":tenant_id".news_feed_status OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 16695)
-- Name: news_store; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".news_store (
    id text NOT NULL,
    title text NOT NULL,
    published_date date NOT NULL,
    country text NOT NULL,
    ksc_name text NOT NULL,
    link text NOT NULL,
    content text NOT NULL,
    source text NOT NULL
);


ALTER TABLE ":tenant_id".news_store OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 16700)
-- Name: news_store2; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".news_store2 (
    id text NOT NULL,
    title text NOT NULL,
    published_date date NOT NULL,
    country text NOT NULL,
    link text NOT NULL,
    description text,
    content text NOT NULL,
    source text NOT NULL,
    category_name text NOT NULL,
    ksc_name text NOT NULL,
    category_id text,
    keyword_id text,
    supplier_id text
);


ALTER TABLE ":tenant_id".news_store2 OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 16705)
-- Name: news_topics; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".news_topics (
    id integer NOT NULL,
    name character varying(500)
);


ALTER TABLE ":tenant_id".news_topics OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 16708)
-- Name: opportunity_insights; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".opportunity_insights (
    category_name text NOT NULL,
    insight_id integer NOT NULL,
    analytics_name text,
    opportunity_insight text,
    impact text,
    linked_insight jsonb,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".opportunity_insights OWNER TO postgres;

--
-- TOC entry 282 (class 1259 OID 16714)
-- Name: sku_qna; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_qna (
    category_name text NOT NULL,
    sku_id text NOT NULL,
    sku_name text,
    qna jsonb,
    period integer DEFAULT 2023 NOT NULL
);


ALTER TABLE ":tenant_id".sku_qna OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 16720)
-- Name: supplier_qna; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".supplier_qna (
    category_name text NOT NULL,
    supplier_name text NOT NULL,
    qna jsonb,
    period integer DEFAULT 2023 NOT NULL
);


ALTER TABLE ":tenant_id".supplier_qna OWNER TO postgres;

--
-- TOC entry 284 (class 1259 OID 16726)
-- Name: qna_view; Type: VIEW; Schema: :tenant_id; Owner: postgres
--

CREATE VIEW ":tenant_id".qna_view AS
 SELECT supplier_qna.supplier_name,
    NULL::text AS sku_id,
    NULL::text AS sku_name,
    supplier_qna.category_name,
    supplier_qna.qna
   FROM ":tenant_id".supplier_qna
UNION ALL
 SELECT NULL::text AS supplier_name,
    sku_qna.sku_id,
    sku_qna.sku_name,
    sku_qna.category_name,
    sku_qna.qna
   FROM ":tenant_id".sku_qna
UNION ALL
 SELECT NULL::text AS supplier_name,
    NULL::text AS sku_id,
    NULL::text AS sku_name,
    category_qna.category_name,
    category_qna.qna
   FROM ":tenant_id".category_qna;


ALTER VIEW ":tenant_id".qna_view OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 16730)
-- Name: requests_status; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".requests_status (
    request_id text,
    use_case text,
    execution_step text,
    execution_percent integer,
    additional_text text,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".requests_status OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 16736)
-- Name: saving_opportunities; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".saving_opportunities (
    supplier_id text NOT NULL,
    supplier_name text,
    category_name text NOT NULL,
    analytics_type text NOT NULL,
    analytics_name text NOT NULL,
    amount double precision,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".saving_opportunities OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 16742)
-- Name: saving_opportunities_copy; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".saving_opportunities_copy (
    supplier_id text NOT NULL,
    supplier_name text,
    category_name text NOT NULL,
    analytics_type text NOT NULL,
    analytics_name text NOT NULL,
    amount double precision,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".saving_opportunities_copy OWNER TO postgres;

--
-- TOC entry 288 (class 1259 OID 16748)
-- Name: saving_opportunities_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".saving_opportunities_final (
    supplier_id text NOT NULL,
    supplier_name text,
    category_name text NOT NULL,
    analytics_type text NOT NULL,
    analytics_name text NOT NULL,
    amount double precision,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".saving_opportunities_final OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 16754)
-- Name: sku_profile; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_profile (
    sku_id text NOT NULL,
    sku_name text,
    category_name text NOT NULL,
    number_of_sku_in_category integer,
    spend_ytd double precision,
    spend_last_year double precision,
    supplier_list jsonb,
    supplier_list_name jsonb,
    percentage_spend_across_category_ytd double precision,
    percentage_spend_across_category_last_year double precision,
    single_source_spend_ytd double precision,
    spend_no_po_ytd double precision,
    payment_terms jsonb,
    payment_term_days jsonb,
    payment_term_avg double precision,
    currency_1 text,
    country text,
    country_cost_type text
);


ALTER TABLE ":tenant_id".sku_profile OWNER TO postgres;

--
-- TOC entry 290 (class 1259 OID 16759)
-- Name: sku_qna_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_qna_final (
    category_name text NOT NULL,
    sku_id text NOT NULL,
    sku_name text,
    qna jsonb
);


ALTER TABLE ":tenant_id".sku_qna_final OWNER TO postgres;

--
-- TOC entry 291 (class 1259 OID 16764)
-- Name: sku_saving_opportunities; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_saving_opportunities (
    sku_id text NOT NULL,
    sku_name text,
    category_name text NOT NULL,
    analytics_type text,
    analytics_name text NOT NULL,
    reporting_currency text,
    amount double precision,
    period integer NOT NULL,
    updated_ts timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE ":tenant_id".sku_saving_opportunities OWNER TO postgres;

--
-- TOC entry 292 (class 1259 OID 16770)
-- Name: sku_supplier_master; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_supplier_master (
    supplier_name text,
    supplier_id text NOT NULL,
    spend_last_year double precision,
    spend_ytd double precision,
    sku_id text NOT NULL,
    sku_name text,
    spend_across_category_ytd double precision,
    spend_across_category_last_year double precision,
    spend_without_po_ytd double precision,
    spend_without_po_last_year double precision,
    spend_single_source_ytd double precision,
    spend_single_source_last_year double precision,
    supplier_relationship text,
    country text,
    country_cost_type text,
    category_name text NOT NULL,
    period integer DEFAULT 2023 NOT NULL,
    contract_count_last_year integer DEFAULT 0,
    contract_count_ytd integer DEFAULT 0,
    invoice_count_last_year integer DEFAULT 0,
    invoice_count_ytd integer DEFAULT 0,
    multi_source_spend_ytd double precision DEFAULT 0.0,
    payment_term_days integer,
    payment_terms text,
    purchase_order_count_last_year integer DEFAULT 0,
    purchase_order_count_ytd integer DEFAULT 0,
    quantity double precision DEFAULT 0.0,
    region text,
    reporting_currency character varying(50) DEFAULT 'EUR'::character varying,
    unit_of_measurement text,
    unit_price double precision DEFAULT 0.0,
    x_axis_condition_1 text,
    x_axis_condition_2 text,
    y_axis_condition_1 text
);


ALTER TABLE ":tenant_id".sku_supplier_master OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 16786)
-- Name: sku_supplier_master_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_supplier_master_final (
    supplier_name text,
    supplier_id text NOT NULL,
    spend_last_year double precision,
    spend_ytd double precision,
    sku_id text NOT NULL,
    sku_name text,
    spend_across_category_ytd double precision,
    spend_across_category_last_year double precision,
    spend_without_po_ytd double precision,
    spend_without_po_last_year double precision,
    spend_single_source_ytd double precision,
    spend_single_source_last_year double precision,
    supplier_relationship text,
    negotiation_strategy text,
    country text,
    hcc text,
    category_name text NOT NULL,
    payment_terms text,
    payment_term_days double precision
);


ALTER TABLE ":tenant_id".sku_supplier_master_final OWNER TO postgres;

--
-- TOC entry 294 (class 1259 OID 16791)
-- Name: sku_supplier_master_vv; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".sku_supplier_master_vv (
    supplier_name text,
    supplier_id text NOT NULL,
    spend_last_year double precision,
    spend_ytd double precision,
    sku_id text NOT NULL,
    sku_name text,
    spend_across_category_ytd double precision,
    spend_across_category_last_year double precision,
    spend_without_po_ytd double precision,
    spend_without_po_last_year double precision,
    spend_single_source_ytd double precision,
    spend_single_source_last_year double precision,
    supplier_relationship text,
    negotiation_strategy text,
    country text,
    hcc text,
    category_name text NOT NULL
);


ALTER TABLE ":tenant_id".sku_supplier_master_vv OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 16796)
-- Name: supplier_news; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".supplier_news (
    news_id text NOT NULL,
    supplier_id text,
    supplier_name text,
    issue_in_webpage_loading text,
    is_relative text,
    news_content text,
    bullet_points_summary jsonb
);


ALTER TABLE ":tenant_id".supplier_news OWNER TO postgres;

--
-- TOC entry 296 (class 1259 OID 16801)
-- Name: supplier_news_view; Type: VIEW; Schema: :tenant_id; Owner: postgres
--

CREATE VIEW ":tenant_id".supplier_news_view AS
 SELECT supplier_news.news_id,
    supplier_news.supplier_id,
    supplier_news.supplier_name,
    supplier_news.news_content,
    supplier_news.bullet_points_summary,
    news.title,
    news.description,
    news.url,
    news.image_url,
    news.publication_date
   FROM (":tenant_id".supplier_news
     JOIN ":tenant_id".news ON ((news.news_id = supplier_news.news_id)))
  WHERE (supplier_news.is_relative = 'Y'::text);


ALTER VIEW ":tenant_id".supplier_news_view OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 16806)
-- Name: supplier_qna_final; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".supplier_qna_final (
    category_name text NOT NULL,
    supplier_name text NOT NULL,
    qna jsonb
);


ALTER TABLE ":tenant_id".supplier_qna_final OWNER TO postgres;

--
-- TOC entry 298 (class 1259 OID 16811)
-- Name: temp_news_store; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".temp_news_store (
    id text NOT NULL,
    title text NOT NULL,
    published_date date NOT NULL,
    country text NOT NULL,
    ksc_name text NOT NULL,
    link text NOT NULL,
    content text NOT NULL,
    source text NOT NULL
);


ALTER TABLE ":tenant_id".temp_news_store OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 16816)
-- Name: top_ideas_example; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".top_ideas_example (
    idea text NOT NULL,
    description text,
    actions text
);


ALTER TABLE ":tenant_id".top_ideas_example OWNER TO postgres;

--
-- TOC entry 300 (class 1259 OID 16821)
-- Name: unified_chat_history; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
)
PARTITION BY RANGE (created_time);


ALTER TABLE ":tenant_id".unified_chat_history OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 16825)
-- Name: unified_chat_history_apr25; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_apr25 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_apr25 OWNER TO postgres;

--
-- TOC entry 302 (class 1259 OID 16831)
-- Name: unified_chat_history_aug24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_aug24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_aug24 OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 16837)
-- Name: unified_chat_history_dec24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_dec24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_dec24 OWNER TO postgres;

--
-- TOC entry 304 (class 1259 OID 16843)
-- Name: unified_chat_history_feb25; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_feb25 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_feb25 OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 16849)
-- Name: unified_chat_history_jan25; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_jan25 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_jan25 OWNER TO postgres;

--
-- TOC entry 306 (class 1259 OID 16855)
-- Name: unified_chat_history_jul24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_jul24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_jul24 OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 16861)
-- Name: unified_chat_history_jun24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_jun24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_jun24 OWNER TO postgres;

--
-- TOC entry 308 (class 1259 OID 16867)
-- Name: unified_chat_history_jun25; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_jun25 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_jun25 OWNER TO postgres;

--
-- TOC entry 309 (class 1259 OID 16873)
-- Name: unified_chat_history_mar25; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_mar25 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_mar25 OWNER TO postgres;

--
-- TOC entry 310 (class 1259 OID 16879)
-- Name: unified_chat_history_may24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_may24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_may24 OWNER TO postgres;

--
-- TOC entry 311 (class 1259 OID 16885)
-- Name: unified_chat_history_may25; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_may25 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_may25 OWNER TO postgres;

--
-- TOC entry 312 (class 1259 OID 16891)
-- Name: unified_chat_history_nov24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_nov24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_nov24 OWNER TO postgres;

--
-- TOC entry 313 (class 1259 OID 16897)
-- Name: unified_chat_history_oct24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_oct24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_oct24 OWNER TO postgres;

--
-- TOC entry 314 (class 1259 OID 16903)
-- Name: unified_chat_history_sep24; Type: TABLE; Schema: :tenant_id; Owner: postgres
--

CREATE TABLE ":tenant_id".unified_chat_history_sep24 (
    chat_id text NOT NULL,
    request_id text NOT NULL,
    request_type text,
    request jsonb,
    model_used text,
    response_type text,
    response jsonb,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE ":tenant_id".unified_chat_history_sep24 OWNER TO postgres;

--
-- TOC entry 4216 (class 0 OID 0)
-- Name: unified_chat_history_apr25; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_apr25 FOR VALUES FROM ('2025-04-01 00:00:00') TO ('2025-05-01 00:00:00');


--
-- TOC entry 4217 (class 0 OID 0)
-- Name: unified_chat_history_aug24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_aug24 FOR VALUES FROM ('2024-08-01 00:00:00') TO ('2024-09-01 00:00:00');


--
-- TOC entry 4218 (class 0 OID 0)
-- Name: unified_chat_history_dec24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_dec24 FOR VALUES FROM ('2024-12-01 00:00:00') TO ('2025-01-01 00:00:00');


--
-- TOC entry 4219 (class 0 OID 0)
-- Name: unified_chat_history_feb25; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_feb25 FOR VALUES FROM ('2025-02-01 00:00:00') TO ('2025-03-01 00:00:00');


--
-- TOC entry 4220 (class 0 OID 0)
-- Name: unified_chat_history_jan25; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_jan25 FOR VALUES FROM ('2025-01-01 00:00:00') TO ('2025-02-01 00:00:00');


--
-- TOC entry 4221 (class 0 OID 0)
-- Name: unified_chat_history_jul24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_jul24 FOR VALUES FROM ('2024-07-01 00:00:00') TO ('2024-08-01 00:00:00');


--
-- TOC entry 4222 (class 0 OID 0)
-- Name: unified_chat_history_jun24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_jun24 FOR VALUES FROM ('2024-06-01 00:00:00') TO ('2024-07-01 00:00:00');


--
-- TOC entry 4223 (class 0 OID 0)
-- Name: unified_chat_history_jun25; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_jun25 FOR VALUES FROM ('2025-06-01 00:00:00') TO ('2025-07-01 00:00:00');


--
-- TOC entry 4224 (class 0 OID 0)
-- Name: unified_chat_history_mar25; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_mar25 FOR VALUES FROM ('2025-03-01 00:00:00') TO ('2025-04-01 00:00:00');


--
-- TOC entry 4225 (class 0 OID 0)
-- Name: unified_chat_history_may24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_may24 FOR VALUES FROM ('2024-05-01 00:00:00') TO ('2024-06-01 00:00:00');


--
-- TOC entry 4226 (class 0 OID 0)
-- Name: unified_chat_history_may25; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_may25 FOR VALUES FROM ('2025-05-01 00:00:00') TO ('2025-06-01 00:00:00');


--
-- TOC entry 4227 (class 0 OID 0)
-- Name: unified_chat_history_nov24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_nov24 FOR VALUES FROM ('2024-11-01 00:00:00') TO ('2024-12-01 00:00:00');


--
-- TOC entry 4228 (class 0 OID 0)
-- Name: unified_chat_history_oct24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_oct24 FOR VALUES FROM ('2024-10-01 00:00:00') TO ('2024-11-01 00:00:00');


--
-- TOC entry 4229 (class 0 OID 0)
-- Name: unified_chat_history_sep24; Type: TABLE ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history ATTACH PARTITION ":tenant_id".unified_chat_history_sep24 FOR VALUES FROM ('2024-09-01 00:00:00') TO ('2024-10-01 00:00:00');


--
-- TOC entry 4236 (class 2604 OID 16909)
-- Name: curated_news_insights id; Type: DEFAULT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".curated_news_insights ALTER COLUMN id SET DEFAULT nextval('":tenant_id".curated_news_insights_id_seq'::regclass);


--
-- TOC entry 4280 (class 2606 OID 45905)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4282 (class 2606 OID 45907)
-- Name: analytics_idea_details analytics_idea_details_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".analytics_idea_details
    ADD CONSTRAINT analytics_idea_details_pkey PRIMARY KEY (category_name, analytics_name);


--
-- TOC entry 4288 (class 2606 OID 45909)
-- Name: categories_news_data categories_news_data_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".categories_news_data
    ADD CONSTRAINT categories_news_data_pkey PRIMARY KEY (news_id);


--
-- TOC entry 4290 (class 2606 OID 45911)
-- Name: category_news category_news_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".category_news
    ADD CONSTRAINT category_news_pkey PRIMARY KEY (news_id);


--
-- TOC entry 4296 (class 2606 OID 45913)
-- Name: category_qna_final category_qna_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".category_qna_final
    ADD CONSTRAINT category_qna_final_pkey PRIMARY KEY (category_name);


--
-- TOC entry 4294 (class 2606 OID 45915)
-- Name: category_qna category_qna_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".category_qna
    ADD CONSTRAINT category_qna_pkey PRIMARY KEY (category_name);


--
-- TOC entry 4300 (class 2606 OID 45917)
-- Name: chat_history_new chat_history_new_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".chat_history_new
    ADD CONSTRAINT chat_history_new_pkey PRIMARY KEY (chat_id);


--
-- TOC entry 4298 (class 2606 OID 45919)
-- Name: chat_history chat_history_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".chat_history
    ADD CONSTRAINT chat_history_pkey PRIMARY KEY (chat_id);


--
-- TOC entry 4302 (class 2606 OID 45921)
-- Name: common_chat_history common_chat_history_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".common_chat_history
    ADD CONSTRAINT common_chat_history_pkey PRIMARY KEY (chat_id, request_id);


--
-- TOC entry 4304 (class 2606 OID 45923)
-- Name: contract_details contract_details_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".contract_details
    ADD CONSTRAINT contract_details_pkey PRIMARY KEY (document_id);


--
-- TOC entry 4306 (class 2606 OID 45925)
-- Name: contract_sku_details contract_sku_details_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".contract_sku_details
    ADD CONSTRAINT contract_sku_details_pkey PRIMARY KEY (document_id, description, sku_id, price);


--
-- TOC entry 4308 (class 2606 OID 45927)
-- Name: curated_news_insights curated_news_insights_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".curated_news_insights
    ADD CONSTRAINT curated_news_insights_pkey PRIMARY KEY (title, topic_name, created_at);


--
-- TOC entry 4312 (class 2606 OID 45929)
-- Name: dashboard_reporting_dummy2 dashboard_reporting_dummy2_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".dashboard_reporting_dummy2
    ADD CONSTRAINT dashboard_reporting_dummy2_pkey PRIMARY KEY (category_name, report_id, sub_report_name);


--
-- TOC entry 4310 (class 2606 OID 45931)
-- Name: dashboard_reporting dashboard_reporting_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".dashboard_reporting
    ADD CONSTRAINT dashboard_reporting_pkey PRIMARY KEY (category_name, report_id, sub_report_name);


--
-- TOC entry 4316 (class 2606 OID 45933)
-- Name: dax_entity_lookup_dummy2 dax_entity_lookup_dummy2_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".dax_entity_lookup_dummy2
    ADD CONSTRAINT dax_entity_lookup_dummy2_pkey PRIMARY KEY (entity_name);


--
-- TOC entry 4314 (class 2606 OID 45935)
-- Name: dax_entity_lookup dax_entity_lookup_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".dax_entity_lookup
    ADD CONSTRAINT dax_entity_lookup_pkey PRIMARY KEY (entity_name, value_range);


--
-- TOC entry 4318 (class 2606 OID 45937)
-- Name: demo_category_qna demo_category_qna_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".demo_category_qna
    ADD CONSTRAINT demo_category_qna_pkey PRIMARY KEY (category_name);


--
-- TOC entry 4320 (class 2606 OID 45939)
-- Name: document_info document_info_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".document_info
    ADD CONSTRAINT document_info_pkey PRIMARY KEY (document_id);


--
-- TOC entry 4322 (class 2606 OID 45941)
-- Name: features features_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".features
    ADD CONSTRAINT features_pkey PRIMARY KEY (feature_name);


--
-- TOC entry 4326 (class 2606 OID 45943)
-- Name: idea_generation_context_dummy idea_generation_context_dummy_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".idea_generation_context_dummy
    ADD CONSTRAINT idea_generation_context_dummy_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4328 (class 2606 OID 45945)
-- Name: idea_generation_context_final idea_generation_context_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".idea_generation_context_final
    ADD CONSTRAINT idea_generation_context_final_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4324 (class 2606 OID 45947)
-- Name: idea_generation_context idea_generation_context_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".idea_generation_context
    ADD CONSTRAINT idea_generation_context_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4332 (class 2606 OID 45949)
-- Name: insights_master_final insights_master_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".insights_master_final
    ADD CONSTRAINT insights_master_final_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4330 (class 2606 OID 45951)
-- Name: insights_master insights_master_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".insights_master
    ADD CONSTRAINT insights_master_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4336 (class 2606 OID 45953)
-- Name: key_facts_config_dummy2 key_facts_config_dummy2_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".key_facts_config_dummy2
    ADD CONSTRAINT key_facts_config_dummy2_pkey PRIMARY KEY (category_name, config_name);


--
-- TOC entry 4334 (class 2606 OID 45955)
-- Name: key_facts_config key_facts_config_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".key_facts_config
    ADD CONSTRAINT key_facts_config_pkey PRIMARY KEY (category_name, config_name);


--
-- TOC entry 4338 (class 2606 OID 45957)
-- Name: keywords_news_data keywords_news_data_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".keywords_news_data
    ADD CONSTRAINT keywords_news_data_pkey PRIMARY KEY (news_id);


--
-- TOC entry 4340 (class 2606 OID 45959)
-- Name: market_approach_strategy_final market_approach_strategy_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".market_approach_strategy_final
    ADD CONSTRAINT market_approach_strategy_final_pkey PRIMARY KEY (market_approach);


--
-- TOC entry 4342 (class 2606 OID 45961)
-- Name: negotiation_chat_history negotiation_chat_history_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_chat_history
    ADD CONSTRAINT negotiation_chat_history_pkey PRIMARY KEY (negotiation_id);


--
-- TOC entry 4344 (class 2606 OID 45963)
-- Name: negotiation_details negotiation_details_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_details
    ADD CONSTRAINT negotiation_details_pkey PRIMARY KEY (negotiation_id);


--
-- TOC entry 4348 (class 2606 OID 45965)
-- Name: negotiation_insights_final negotiation_insights_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_insights_final
    ADD CONSTRAINT negotiation_insights_final_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4346 (class 2606 OID 45967)
-- Name: negotiation_insights negotiation_insights_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_insights
    ADD CONSTRAINT negotiation_insights_pkey PRIMARY KEY (insight_id);


--
-- TOC entry 4354 (class 2606 OID 45969)
-- Name: negotiation_relationship_details_final negotiation_relationship_details_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_relationship_details_final
    ADD CONSTRAINT negotiation_relationship_details_final_pkey PRIMARY KEY (relationship);


--
-- TOC entry 4356 (class 2606 OID 45971)
-- Name: negotiation_strategy_details_final negotiation_strategy_details_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_strategy_details_final
    ADD CONSTRAINT negotiation_strategy_details_final_pkey PRIMARY KEY (category_name);


--
-- TOC entry 4358 (class 2606 OID 45973)
-- Name: negotiation_strategy_tones_n_tactics negotiation_strategy_tones_n_tactics_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_strategy_tones_n_tactics
    ADD CONSTRAINT negotiation_strategy_tones_n_tactics_pkey PRIMARY KEY (tone_name, supplier_positioning);


--
-- TOC entry 4292 (class 2606 OID 45975)
-- Name: news news_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".news
    ADD CONSTRAINT news_pkey PRIMARY KEY (news_id);


--
-- TOC entry 4364 (class 2606 OID 45977)
-- Name: news_store2 news_store2_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".news_store2
    ADD CONSTRAINT news_store2_pkey PRIMARY KEY (id);


--
-- TOC entry 4362 (class 2606 OID 45979)
-- Name: news_store news_store_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".news_store
    ADD CONSTRAINT news_store_pkey PRIMARY KEY (id);


--
-- TOC entry 4366 (class 2606 OID 45981)
-- Name: news_topics news_topics_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".news_topics
    ADD CONSTRAINT news_topics_pkey PRIMARY KEY (id);


--
-- TOC entry 4368 (class 2606 OID 45983)
-- Name: opportunity_insights opportunity_insights_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".opportunity_insights
    ADD CONSTRAINT opportunity_insights_pkey PRIMARY KEY (category_name, insight_id);


--
-- TOC entry 4350 (class 2606 OID 45985)
-- Name: negotiation_objective pk_negotiation_objective; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_objective
    ADD CONSTRAINT pk_negotiation_objective PRIMARY KEY (supplier_id, objective, category_name);


--
-- TOC entry 4352 (class 2606 OID 45987)
-- Name: negotiation_objective_final pk_negotiation_objective_final; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".negotiation_objective_final
    ADD CONSTRAINT pk_negotiation_objective_final PRIMARY KEY (supplier_id, objective, category_name);


--
-- TOC entry 4374 (class 2606 OID 45989)
-- Name: saving_opportunities pk_saving_opportunities; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".saving_opportunities
    ADD CONSTRAINT pk_saving_opportunities PRIMARY KEY (supplier_id, category_name, analytics_type, analytics_name);


--
-- TOC entry 4376 (class 2606 OID 45991)
-- Name: saving_opportunities_copy pk_saving_opportunities_copy; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".saving_opportunities_copy
    ADD CONSTRAINT pk_saving_opportunities_copy PRIMARY KEY (supplier_id, category_name, analytics_type, analytics_name);


--
-- TOC entry 4378 (class 2606 OID 45993)
-- Name: saving_opportunities_final pk_saving_opportunities_final; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".saving_opportunities_final
    ADD CONSTRAINT pk_saving_opportunities_final PRIMARY KEY (supplier_id, category_name, analytics_type, analytics_name);


--
-- TOC entry 4384 (class 2606 OID 45995)
-- Name: sku_saving_opportunities pk_sku_saving_opportunities; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_saving_opportunities
    ADD CONSTRAINT pk_sku_saving_opportunities PRIMARY KEY (sku_id, category_name, analytics_name, period);


--
-- TOC entry 4386 (class 2606 OID 45997)
-- Name: sku_supplier_master pk_supplier_profile; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_supplier_master
    ADD CONSTRAINT pk_supplier_profile PRIMARY KEY (supplier_id, sku_id, category_name, period);


--
-- TOC entry 4388 (class 2606 OID 45999)
-- Name: sku_supplier_master_final pk_supplier_profile_final; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_supplier_master_final
    ADD CONSTRAINT pk_supplier_profile_final PRIMARY KEY (supplier_id, sku_id, category_name);


--
-- TOC entry 4390 (class 2606 OID 46001)
-- Name: sku_supplier_master_vv pk_supplier_profile_vv; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_supplier_master_vv
    ADD CONSTRAINT pk_supplier_profile_vv PRIMARY KEY (supplier_id, sku_id, category_name);


--
-- TOC entry 4380 (class 2606 OID 46003)
-- Name: sku_profile sku_profile_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_profile
    ADD CONSTRAINT sku_profile_pkey PRIMARY KEY (sku_id, category_name);


--
-- TOC entry 4382 (class 2606 OID 46005)
-- Name: sku_qna_final sku_qna_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_qna_final
    ADD CONSTRAINT sku_qna_final_pkey PRIMARY KEY (category_name, sku_id);


--
-- TOC entry 4370 (class 2606 OID 46007)
-- Name: sku_qna sku_qna_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".sku_qna
    ADD CONSTRAINT sku_qna_pkey PRIMARY KEY (sku_id, category_name, period);


--
-- TOC entry 4392 (class 2606 OID 46009)
-- Name: supplier_news supplier_news_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".supplier_news
    ADD CONSTRAINT supplier_news_pkey PRIMARY KEY (news_id);


--
-- TOC entry 4394 (class 2606 OID 46011)
-- Name: supplier_qna_final supplier_qna_final_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".supplier_qna_final
    ADD CONSTRAINT supplier_qna_final_pkey PRIMARY KEY (category_name, supplier_name);


--
-- TOC entry 4372 (class 2606 OID 46013)
-- Name: supplier_qna supplier_qna_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".supplier_qna
    ADD CONSTRAINT supplier_qna_pkey PRIMARY KEY (supplier_name, category_name, period);


--
-- TOC entry 4360 (class 2606 OID 46015)
-- Name: suppliers_news_data suppliers_news_data_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".suppliers_news_data
    ADD CONSTRAINT suppliers_news_data_pkey PRIMARY KEY (news_id);


--
-- TOC entry 4396 (class 2606 OID 46017)
-- Name: temp_news_store temp_news_store_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".temp_news_store
    ADD CONSTRAINT temp_news_store_pkey PRIMARY KEY (id);


--
-- TOC entry 4284 (class 2606 OID 46019)
-- Name: top_idea_details top_idea_details_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".top_idea_details
    ADD CONSTRAINT top_idea_details_pkey PRIMARY KEY (category_name, file_timestamp, idea_number);


--
-- TOC entry 4398 (class 2606 OID 46021)
-- Name: top_ideas_example top_ideas_example_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".top_ideas_example
    ADD CONSTRAINT top_ideas_example_pkey PRIMARY KEY (idea);


--
-- TOC entry 4286 (class 2606 OID 46023)
-- Name: top_ideas_knowledge_base top_ideas_knowledge_base_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".top_ideas_knowledge_base
    ADD CONSTRAINT top_ideas_knowledge_base_pkey PRIMARY KEY (category_name, analytics_name);


--
-- TOC entry 4401 (class 2606 OID 46025)
-- Name: unified_chat_history unified_chat_history_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history
    ADD CONSTRAINT unified_chat_history_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4404 (class 2606 OID 46027)
-- Name: unified_chat_history_apr25 unified_chat_history_apr25_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_apr25
    ADD CONSTRAINT unified_chat_history_apr25_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4407 (class 2606 OID 46029)
-- Name: unified_chat_history_aug24 unified_chat_history_aug24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_aug24
    ADD CONSTRAINT unified_chat_history_aug24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4410 (class 2606 OID 46031)
-- Name: unified_chat_history_dec24 unified_chat_history_dec24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_dec24
    ADD CONSTRAINT unified_chat_history_dec24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4413 (class 2606 OID 46033)
-- Name: unified_chat_history_feb25 unified_chat_history_feb25_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_feb25
    ADD CONSTRAINT unified_chat_history_feb25_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4416 (class 2606 OID 46035)
-- Name: unified_chat_history_jan25 unified_chat_history_jan25_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_jan25
    ADD CONSTRAINT unified_chat_history_jan25_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4419 (class 2606 OID 46037)
-- Name: unified_chat_history_jul24 unified_chat_history_jul24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_jul24
    ADD CONSTRAINT unified_chat_history_jul24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4422 (class 2606 OID 46039)
-- Name: unified_chat_history_jun24 unified_chat_history_jun24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_jun24
    ADD CONSTRAINT unified_chat_history_jun24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4425 (class 2606 OID 46041)
-- Name: unified_chat_history_jun25 unified_chat_history_jun25_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_jun25
    ADD CONSTRAINT unified_chat_history_jun25_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4428 (class 2606 OID 46043)
-- Name: unified_chat_history_mar25 unified_chat_history_mar25_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_mar25
    ADD CONSTRAINT unified_chat_history_mar25_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4431 (class 2606 OID 46045)
-- Name: unified_chat_history_may24 unified_chat_history_may24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_may24
    ADD CONSTRAINT unified_chat_history_may24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4434 (class 2606 OID 46047)
-- Name: unified_chat_history_may25 unified_chat_history_may25_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_may25
    ADD CONSTRAINT unified_chat_history_may25_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4437 (class 2606 OID 46049)
-- Name: unified_chat_history_nov24 unified_chat_history_nov24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_nov24
    ADD CONSTRAINT unified_chat_history_nov24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4440 (class 2606 OID 46051)
-- Name: unified_chat_history_oct24 unified_chat_history_oct24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_oct24
    ADD CONSTRAINT unified_chat_history_oct24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4443 (class 2606 OID 46053)
-- Name: unified_chat_history_sep24 unified_chat_history_sep24_pkey; Type: CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".unified_chat_history_sep24
    ADD CONSTRAINT unified_chat_history_sep24_pkey PRIMARY KEY (chat_id, request_id, created_time);


--
-- TOC entry 4399 (class 1259 OID 46054)
-- Name: idx_unified_chat_history_chat_id; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX idx_unified_chat_history_chat_id ON ONLY ":tenant_id".unified_chat_history USING btree (chat_id);


--
-- TOC entry 4402 (class 1259 OID 46055)
-- Name: unified_chat_history_apr25_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_apr25_chat_id_idx ON ":tenant_id".unified_chat_history_apr25 USING btree (chat_id);


--
-- TOC entry 4405 (class 1259 OID 46056)
-- Name: unified_chat_history_aug24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_aug24_chat_id_idx ON ":tenant_id".unified_chat_history_aug24 USING btree (chat_id);


--
-- TOC entry 4408 (class 1259 OID 46057)
-- Name: unified_chat_history_dec24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_dec24_chat_id_idx ON ":tenant_id".unified_chat_history_dec24 USING btree (chat_id);


--
-- TOC entry 4411 (class 1259 OID 46058)
-- Name: unified_chat_history_feb25_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_feb25_chat_id_idx ON ":tenant_id".unified_chat_history_feb25 USING btree (chat_id);


--
-- TOC entry 4414 (class 1259 OID 46059)
-- Name: unified_chat_history_jan25_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_jan25_chat_id_idx ON ":tenant_id".unified_chat_history_jan25 USING btree (chat_id);


--
-- TOC entry 4417 (class 1259 OID 46060)
-- Name: unified_chat_history_jul24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_jul24_chat_id_idx ON ":tenant_id".unified_chat_history_jul24 USING btree (chat_id);


--
-- TOC entry 4420 (class 1259 OID 46061)
-- Name: unified_chat_history_jun24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_jun24_chat_id_idx ON ":tenant_id".unified_chat_history_jun24 USING btree (chat_id);


--
-- TOC entry 4423 (class 1259 OID 46062)
-- Name: unified_chat_history_jun25_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_jun25_chat_id_idx ON ":tenant_id".unified_chat_history_jun25 USING btree (chat_id);


--
-- TOC entry 4426 (class 1259 OID 46063)
-- Name: unified_chat_history_mar25_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_mar25_chat_id_idx ON ":tenant_id".unified_chat_history_mar25 USING btree (chat_id);


--
-- TOC entry 4429 (class 1259 OID 46064)
-- Name: unified_chat_history_may24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_may24_chat_id_idx ON ":tenant_id".unified_chat_history_may24 USING btree (chat_id);


--
-- TOC entry 4432 (class 1259 OID 46065)
-- Name: unified_chat_history_may25_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_may25_chat_id_idx ON ":tenant_id".unified_chat_history_may25 USING btree (chat_id);


--
-- TOC entry 4435 (class 1259 OID 46066)
-- Name: unified_chat_history_nov24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_nov24_chat_id_idx ON ":tenant_id".unified_chat_history_nov24 USING btree (chat_id);


--
-- TOC entry 4438 (class 1259 OID 46067)
-- Name: unified_chat_history_oct24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_oct24_chat_id_idx ON ":tenant_id".unified_chat_history_oct24 USING btree (chat_id);


--
-- TOC entry 4441 (class 1259 OID 46068)
-- Name: unified_chat_history_sep24_chat_id_idx; Type: INDEX; Schema: :tenant_id; Owner: postgres
--

CREATE INDEX unified_chat_history_sep24_chat_id_idx ON ":tenant_id".unified_chat_history_sep24 USING btree (chat_id);


--
-- TOC entry 4444 (class 0 OID 0)
-- Name: unified_chat_history_apr25_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_apr25_chat_id_idx;


--
-- TOC entry 4445 (class 0 OID 0)
-- Name: unified_chat_history_apr25_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_apr25_pkey;


--
-- TOC entry 4446 (class 0 OID 0)
-- Name: unified_chat_history_aug24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_aug24_chat_id_idx;


--
-- TOC entry 4447 (class 0 OID 0)
-- Name: unified_chat_history_aug24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_aug24_pkey;


--
-- TOC entry 4448 (class 0 OID 0)
-- Name: unified_chat_history_dec24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_dec24_chat_id_idx;


--
-- TOC entry 4449 (class 0 OID 0)
-- Name: unified_chat_history_dec24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_dec24_pkey;


--
-- TOC entry 4450 (class 0 OID 0)
-- Name: unified_chat_history_feb25_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_feb25_chat_id_idx;


--
-- TOC entry 4451 (class 0 OID 0)
-- Name: unified_chat_history_feb25_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_feb25_pkey;


--
-- TOC entry 4452 (class 0 OID 0)
-- Name: unified_chat_history_jan25_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_jan25_chat_id_idx;


--
-- TOC entry 4453 (class 0 OID 0)
-- Name: unified_chat_history_jan25_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_jan25_pkey;


--
-- TOC entry 4454 (class 0 OID 0)
-- Name: unified_chat_history_jul24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_jul24_chat_id_idx;


--
-- TOC entry 4455 (class 0 OID 0)
-- Name: unified_chat_history_jul24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_jul24_pkey;


--
-- TOC entry 4456 (class 0 OID 0)
-- Name: unified_chat_history_jun24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_jun24_chat_id_idx;


--
-- TOC entry 4457 (class 0 OID 0)
-- Name: unified_chat_history_jun24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_jun24_pkey;


--
-- TOC entry 4458 (class 0 OID 0)
-- Name: unified_chat_history_jun25_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_jun25_chat_id_idx;


--
-- TOC entry 4459 (class 0 OID 0)
-- Name: unified_chat_history_jun25_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_jun25_pkey;


--
-- TOC entry 4460 (class 0 OID 0)
-- Name: unified_chat_history_mar25_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_mar25_chat_id_idx;


--
-- TOC entry 4461 (class 0 OID 0)
-- Name: unified_chat_history_mar25_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_mar25_pkey;


--
-- TOC entry 4462 (class 0 OID 0)
-- Name: unified_chat_history_may24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_may24_chat_id_idx;


--
-- TOC entry 4463 (class 0 OID 0)
-- Name: unified_chat_history_may24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_may24_pkey;


--
-- TOC entry 4464 (class 0 OID 0)
-- Name: unified_chat_history_may25_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_may25_chat_id_idx;


--
-- TOC entry 4465 (class 0 OID 0)
-- Name: unified_chat_history_may25_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_may25_pkey;


--
-- TOC entry 4466 (class 0 OID 0)
-- Name: unified_chat_history_nov24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_nov24_chat_id_idx;


--
-- TOC entry 4467 (class 0 OID 0)
-- Name: unified_chat_history_nov24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_nov24_pkey;


--
-- TOC entry 4468 (class 0 OID 0)
-- Name: unified_chat_history_oct24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_oct24_chat_id_idx;


--
-- TOC entry 4469 (class 0 OID 0)
-- Name: unified_chat_history_oct24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_oct24_pkey;


--
-- TOC entry 4470 (class 0 OID 0)
-- Name: unified_chat_history_sep24_chat_id_idx; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".idx_unified_chat_history_chat_id ATTACH PARTITION ":tenant_id".unified_chat_history_sep24_chat_id_idx;


--
-- TOC entry 4471 (class 0 OID 0)
-- Name: unified_chat_history_sep24_pkey; Type: INDEX ATTACH; Schema: :tenant_id; Owner: postgres
--

ALTER INDEX ":tenant_id".unified_chat_history_pkey ATTACH PARTITION ":tenant_id".unified_chat_history_sep24_pkey;


--
-- TOC entry 4472 (class 2606 OID 46069)
-- Name: category_news category_news_news_id_fkey; Type: FK CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".category_news
    ADD CONSTRAINT category_news_news_id_fkey FOREIGN KEY (news_id) REFERENCES ":tenant_id".news(news_id);


--
-- TOC entry 4473 (class 2606 OID 46074)
-- Name: supplier_news supplier_news_news_id_fkey; Type: FK CONSTRAINT; Schema: :tenant_id; Owner: postgres
--

ALTER TABLE ONLY ":tenant_id".supplier_news
    ADD CONSTRAINT supplier_news_news_id_fkey FOREIGN KEY (news_id) REFERENCES ":tenant_id".news(news_id);


--
-- TOC entry 4634 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE alembic_version; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".alembic_version TO ":tenant_id";


--
-- TOC entry 4635 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE analytics_idea_details; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".analytics_idea_details TO ":tenant_id";


--
-- TOC entry 4636 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE top_idea_details; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".top_idea_details TO ":tenant_id";


--
-- TOC entry 4637 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE top_ideas_knowledge_base; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".top_ideas_knowledge_base TO ":tenant_id";


--
-- TOC entry 4638 (class 0 OID 0)
-- Dependencies: 233
-- Name: TABLE analytics_ideas_opportunities_view; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".analytics_ideas_opportunities_view TO ":tenant_id";


--
-- TOC entry 4639 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE categories; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".categories TO ":tenant_id";


--
-- TOC entry 4640 (class 0 OID 0)
-- Dependencies: 235
-- Name: TABLE categories_news_data; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".categories_news_data TO ":tenant_id";


--
-- TOC entry 4641 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE category_news; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".category_news TO ":tenant_id";


--
-- TOC entry 4642 (class 0 OID 0)
-- Dependencies: 237
-- Name: TABLE news; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".news TO ":tenant_id";


--
-- TOC entry 4643 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE category_news_view; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".category_news_view TO ":tenant_id";


--
-- TOC entry 4644 (class 0 OID 0)
-- Dependencies: 239
-- Name: TABLE category_qna; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".category_qna TO ":tenant_id";


--
-- TOC entry 4645 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE category_qna_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".category_qna_final TO ":tenant_id";


--
-- TOC entry 4646 (class 0 OID 0)
-- Dependencies: 241
-- Name: TABLE chat_history; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".chat_history TO ":tenant_id";


--
-- TOC entry 4647 (class 0 OID 0)
-- Dependencies: 242
-- Name: TABLE chat_history_new; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".chat_history_new TO ":tenant_id";


--
-- TOC entry 4648 (class 0 OID 0)
-- Dependencies: 243
-- Name: SEQUENCE chat_id_sequence; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT ALL ON SEQUENCE ":tenant_id".chat_id_sequence TO ":tenant_id";


--
-- TOC entry 4649 (class 0 OID 0)
-- Dependencies: 244
-- Name: TABLE common_chat_history; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".common_chat_history TO ":tenant_id";


--
-- TOC entry 4650 (class 0 OID 0)
-- Dependencies: 245
-- Name: TABLE contract_details; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".contract_details TO ":tenant_id";


--
-- TOC entry 4651 (class 0 OID 0)
-- Dependencies: 246
-- Name: TABLE contract_sku_details; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".contract_sku_details TO ":tenant_id";


--
-- TOC entry 4652 (class 0 OID 0)
-- Dependencies: 247
-- Name: TABLE curated_news_insights; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".curated_news_insights TO ":tenant_id";


--
-- TOC entry 4654 (class 0 OID 0)
-- Dependencies: 248
-- Name: SEQUENCE curated_news_insights_id_seq; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT ALL ON SEQUENCE ":tenant_id".curated_news_insights_id_seq TO ":tenant_id";


--
-- TOC entry 4655 (class 0 OID 0)
-- Dependencies: 249
-- Name: TABLE dashboard_reporting; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".dashboard_reporting TO ":tenant_id";


--
-- TOC entry 4656 (class 0 OID 0)
-- Dependencies: 250
-- Name: TABLE dashboard_reporting_dummy2; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".dashboard_reporting_dummy2 TO ":tenant_id";


--
-- TOC entry 4657 (class 0 OID 0)
-- Dependencies: 251
-- Name: TABLE dax_entity_lookup; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".dax_entity_lookup TO ":tenant_id";


--
-- TOC entry 4658 (class 0 OID 0)
-- Dependencies: 252
-- Name: TABLE dax_entity_lookup_dummy2; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".dax_entity_lookup_dummy2 TO ":tenant_id";


--
-- TOC entry 4659 (class 0 OID 0)
-- Dependencies: 253
-- Name: TABLE demo_category_qna; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".demo_category_qna TO ":tenant_id";


--
-- TOC entry 4660 (class 0 OID 0)
-- Dependencies: 254
-- Name: TABLE document_info; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".document_info TO ":tenant_id";


--
-- TOC entry 4661 (class 0 OID 0)
-- Dependencies: 255
-- Name: TABLE features; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".features TO ":tenant_id";


--
-- TOC entry 4662 (class 0 OID 0)
-- Dependencies: 256
-- Name: TABLE idea_generation_context; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".idea_generation_context TO ":tenant_id";


--
-- TOC entry 4663 (class 0 OID 0)
-- Dependencies: 257
-- Name: TABLE idea_generation_context_dummy; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".idea_generation_context_dummy TO ":tenant_id";


--
-- TOC entry 4664 (class 0 OID 0)
-- Dependencies: 258
-- Name: TABLE idea_generation_context_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".idea_generation_context_final TO ":tenant_id";


--
-- TOC entry 4665 (class 0 OID 0)
-- Dependencies: 259
-- Name: TABLE insights_master; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".insights_master TO ":tenant_id";


--
-- TOC entry 4666 (class 0 OID 0)
-- Dependencies: 260
-- Name: TABLE insights_master_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".insights_master_final TO ":tenant_id";


--
-- TOC entry 4667 (class 0 OID 0)
-- Dependencies: 261
-- Name: TABLE key_facts_config; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".key_facts_config TO ":tenant_id";


--
-- TOC entry 4668 (class 0 OID 0)
-- Dependencies: 262
-- Name: TABLE key_facts_config_dummy2; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".key_facts_config_dummy2 TO ":tenant_id";


--
-- TOC entry 4669 (class 0 OID 0)
-- Dependencies: 263
-- Name: TABLE keywords_news_data; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".keywords_news_data TO ":tenant_id";


--
-- TOC entry 4670 (class 0 OID 0)
-- Dependencies: 264
-- Name: TABLE market_approach_strategy_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".market_approach_strategy_final TO ":tenant_id";


--
-- TOC entry 4671 (class 0 OID 0)
-- Dependencies: 265
-- Name: TABLE negotiation_chat_history; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_chat_history TO ":tenant_id";


--
-- TOC entry 4672 (class 0 OID 0)
-- Dependencies: 266
-- Name: TABLE negotiation_details; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_details TO ":tenant_id";


--
-- TOC entry 4673 (class 0 OID 0)
-- Dependencies: 267
-- Name: TABLE negotiation_insights; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_insights TO ":tenant_id";


--
-- TOC entry 4674 (class 0 OID 0)
-- Dependencies: 268
-- Name: TABLE negotiation_insights_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_insights_final TO ":tenant_id";


--
-- TOC entry 4675 (class 0 OID 0)
-- Dependencies: 269
-- Name: TABLE negotiation_objective; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_objective TO ":tenant_id";


--
-- TOC entry 4676 (class 0 OID 0)
-- Dependencies: 270
-- Name: TABLE negotiation_objective_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_objective_final TO ":tenant_id";


--
-- TOC entry 4677 (class 0 OID 0)
-- Dependencies: 271
-- Name: TABLE negotiation_references_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_references_final TO ":tenant_id";


--
-- TOC entry 4678 (class 0 OID 0)
-- Dependencies: 272
-- Name: TABLE negotiation_relationship_details_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_relationship_details_final TO ":tenant_id";


--
-- TOC entry 4679 (class 0 OID 0)
-- Dependencies: 273
-- Name: TABLE negotiation_strategy_details_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_strategy_details_final TO ":tenant_id";


--
-- TOC entry 4680 (class 0 OID 0)
-- Dependencies: 274
-- Name: TABLE negotiation_strategy_tones_n_tactics; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".negotiation_strategy_tones_n_tactics TO ":tenant_id";


--
-- TOC entry 4681 (class 0 OID 0)
-- Dependencies: 275
-- Name: TABLE suppliers_news_data; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".suppliers_news_data TO ":tenant_id";


--
-- TOC entry 4682 (class 0 OID 0)
-- Dependencies: 276
-- Name: TABLE news_aggregations; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".news_aggregations TO ":tenant_id";


--
-- TOC entry 4683 (class 0 OID 0)
-- Dependencies: 277
-- Name: TABLE news_feed_status; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".news_feed_status TO ":tenant_id";


--
-- TOC entry 4684 (class 0 OID 0)
-- Dependencies: 278
-- Name: TABLE news_store; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".news_store TO ":tenant_id";


--
-- TOC entry 4685 (class 0 OID 0)
-- Dependencies: 279
-- Name: TABLE news_store2; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".news_store2 TO ":tenant_id";


--
-- TOC entry 4686 (class 0 OID 0)
-- Dependencies: 280
-- Name: TABLE news_topics; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".news_topics TO ":tenant_id";


--
-- TOC entry 4687 (class 0 OID 0)
-- Dependencies: 281
-- Name: TABLE opportunity_insights; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".opportunity_insights TO ":tenant_id";


--
-- TOC entry 4688 (class 0 OID 0)
-- Dependencies: 282
-- Name: TABLE sku_qna; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_qna TO ":tenant_id";


--
-- TOC entry 4689 (class 0 OID 0)
-- Dependencies: 283
-- Name: TABLE supplier_qna; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".supplier_qna TO ":tenant_id";


--
-- TOC entry 4690 (class 0 OID 0)
-- Dependencies: 284
-- Name: TABLE qna_view; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".qna_view TO ":tenant_id";


--
-- TOC entry 4691 (class 0 OID 0)
-- Dependencies: 285
-- Name: TABLE requests_status; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".requests_status TO ":tenant_id";


--
-- TOC entry 4692 (class 0 OID 0)
-- Dependencies: 286
-- Name: TABLE saving_opportunities; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".saving_opportunities TO ":tenant_id";


--
-- TOC entry 4693 (class 0 OID 0)
-- Dependencies: 287
-- Name: TABLE saving_opportunities_copy; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".saving_opportunities_copy TO ":tenant_id";


--
-- TOC entry 4694 (class 0 OID 0)
-- Dependencies: 288
-- Name: TABLE saving_opportunities_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".saving_opportunities_final TO ":tenant_id";


--
-- TOC entry 4695 (class 0 OID 0)
-- Dependencies: 289
-- Name: TABLE sku_profile; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_profile TO ":tenant_id";


--
-- TOC entry 4696 (class 0 OID 0)
-- Dependencies: 290
-- Name: TABLE sku_qna_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_qna_final TO ":tenant_id";


--
-- TOC entry 4697 (class 0 OID 0)
-- Dependencies: 291
-- Name: TABLE sku_saving_opportunities; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_saving_opportunities TO ":tenant_id";


--
-- TOC entry 4698 (class 0 OID 0)
-- Dependencies: 292
-- Name: TABLE sku_supplier_master; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_supplier_master TO ":tenant_id";


--
-- TOC entry 4699 (class 0 OID 0)
-- Dependencies: 293
-- Name: TABLE sku_supplier_master_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_supplier_master_final TO ":tenant_id";


--
-- TOC entry 4700 (class 0 OID 0)
-- Dependencies: 294
-- Name: TABLE sku_supplier_master_vv; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".sku_supplier_master_vv TO ":tenant_id";


--
-- TOC entry 4701 (class 0 OID 0)
-- Dependencies: 295
-- Name: TABLE supplier_news; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".supplier_news TO ":tenant_id";


--
-- TOC entry 4702 (class 0 OID 0)
-- Dependencies: 296
-- Name: TABLE supplier_news_view; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".supplier_news_view TO ":tenant_id";


--
-- TOC entry 4703 (class 0 OID 0)
-- Dependencies: 297
-- Name: TABLE supplier_qna_final; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".supplier_qna_final TO ":tenant_id";


--
-- TOC entry 4704 (class 0 OID 0)
-- Dependencies: 298
-- Name: TABLE temp_news_store; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".temp_news_store TO ":tenant_id";


--
-- TOC entry 4705 (class 0 OID 0)
-- Dependencies: 299
-- Name: TABLE top_ideas_example; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".top_ideas_example TO ":tenant_id";


--
-- TOC entry 4706 (class 0 OID 0)
-- Dependencies: 300
-- Name: TABLE unified_chat_history; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history TO ":tenant_id";


--
-- TOC entry 4707 (class 0 OID 0)
-- Dependencies: 301
-- Name: TABLE unified_chat_history_apr25; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_apr25 TO ":tenant_id";


--
-- TOC entry 4708 (class 0 OID 0)
-- Dependencies: 302
-- Name: TABLE unified_chat_history_aug24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_aug24 TO ":tenant_id";


--
-- TOC entry 4709 (class 0 OID 0)
-- Dependencies: 303
-- Name: TABLE unified_chat_history_dec24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_dec24 TO ":tenant_id";


--
-- TOC entry 4710 (class 0 OID 0)
-- Dependencies: 304
-- Name: TABLE unified_chat_history_feb25; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_feb25 TO ":tenant_id";


--
-- TOC entry 4711 (class 0 OID 0)
-- Dependencies: 305
-- Name: TABLE unified_chat_history_jan25; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_jan25 TO ":tenant_id";


--
-- TOC entry 4712 (class 0 OID 0)
-- Dependencies: 306
-- Name: TABLE unified_chat_history_jul24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_jul24 TO ":tenant_id";


--
-- TOC entry 4713 (class 0 OID 0)
-- Dependencies: 307
-- Name: TABLE unified_chat_history_jun24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_jun24 TO ":tenant_id";


--
-- TOC entry 4714 (class 0 OID 0)
-- Dependencies: 308
-- Name: TABLE unified_chat_history_jun25; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_jun25 TO ":tenant_id";


--
-- TOC entry 4715 (class 0 OID 0)
-- Dependencies: 309
-- Name: TABLE unified_chat_history_mar25; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_mar25 TO ":tenant_id";


--
-- TOC entry 4716 (class 0 OID 0)
-- Dependencies: 310
-- Name: TABLE unified_chat_history_may24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_may24 TO ":tenant_id";


--
-- TOC entry 4717 (class 0 OID 0)
-- Dependencies: 311
-- Name: TABLE unified_chat_history_may25; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_may25 TO ":tenant_id";


--
-- TOC entry 4718 (class 0 OID 0)
-- Dependencies: 312
-- Name: TABLE unified_chat_history_nov24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_nov24 TO ":tenant_id";


--
-- TOC entry 4719 (class 0 OID 0)
-- Dependencies: 313
-- Name: TABLE unified_chat_history_oct24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_oct24 TO ":tenant_id";


--
-- TOC entry 4720 (class 0 OID 0)
-- Dependencies: 314
-- Name: TABLE unified_chat_history_sep24; Type: ACL; Schema: :tenant_id; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE ":tenant_id".unified_chat_history_sep24 TO ":tenant_id";


-- Completed on 2025-04-02 18:56:13 IST

--
-- PostgreSQL database dump complete
--

