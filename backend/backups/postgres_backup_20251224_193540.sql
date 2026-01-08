--
-- PostgreSQL database dump
--

\restrict oELYTukfHwkq9KydPldrkCkPGxwfF8x5G7dIXUnoG6UdrNE0rhAmMrH1wNtLHc1

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

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
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO raven_user;

--
-- Name: configuration_types; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.configuration_types (
    id integer NOT NULL,
    config_name character varying(100) NOT NULL,
    config_code character varying(20) NOT NULL,
    panel_count integer NOT NULL,
    operable_panels integer NOT NULL,
    panel_indicator_style character varying(50),
    requires_mullions boolean DEFAULT false,
    requires_hardware boolean DEFAULT true,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.configuration_types OWNER TO raven_user;

--
-- Name: TABLE configuration_types; Type: COMMENT; Schema: public; Owner: raven_user
--

COMMENT ON TABLE public.configuration_types IS 'Reference data for window/door configurations (Fixed, Casement, Slider, etc.)';


--
-- Name: configuration_types_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.configuration_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.configuration_types_id_seq OWNER TO raven_user;

--
-- Name: configuration_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.configuration_types_id_seq OWNED BY public.configuration_types.id;


--
-- Name: doors; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.doors (
    id integer NOT NULL,
    project_id integer,
    item_number character varying(50) NOT NULL,
    room character varying(100),
    width_inches numeric(10,2),
    height_inches numeric(10,2),
    door_type character varying(50),
    frame_series character varying(20),
    swing_direction character varying(50),
    quantity integer,
    frame_color character varying(50),
    glass_type character varying(100),
    threshold character varying(50),
    sill_pan_depth numeric(10,2),
    sill_pan_length numeric(10,2),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.doors OWNER TO raven_user;

--
-- Name: doors_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.doors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doors_id_seq OWNER TO raven_user;

--
-- Name: doors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.doors_id_seq OWNED BY public.doors.id;


--
-- Name: frame_colors; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.frame_colors (
    id integer NOT NULL,
    color_name character varying(100) NOT NULL,
    color_code character varying(20),
    hex_value character varying(7),
    rgb_value character varying(50),
    finish_type character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.frame_colors OWNER TO raven_user;

--
-- Name: TABLE frame_colors; Type: COMMENT; Schema: public; Owner: raven_user
--

COMMENT ON TABLE public.frame_colors IS 'Reference data for frame color finishes';


--
-- Name: frame_colors_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.frame_colors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.frame_colors_id_seq OWNER TO raven_user;

--
-- Name: frame_colors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.frame_colors_id_seq OWNED BY public.frame_colors.id;


--
-- Name: frame_series; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.frame_series (
    id integer NOT NULL,
    series_name character varying(50) NOT NULL,
    series_code character varying(20) NOT NULL,
    frame_width_mm numeric(10,2) NOT NULL,
    sash_width_mm numeric(10,2),
    nail_fin_width_mm numeric(10,2) DEFAULT 30.00,
    nail_fin_height_mm numeric(10,2) DEFAULT 30.00,
    thermal_break boolean DEFAULT true,
    glass_pocket_depth_mm numeric(10,2),
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.frame_series OWNER TO raven_user;

--
-- Name: TABLE frame_series; Type: COMMENT; Schema: public; Owner: raven_user
--

COMMENT ON TABLE public.frame_series IS 'Reference data for frame profiles (Series 80, 86, 135, etc.)';


--
-- Name: frame_series_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.frame_series_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.frame_series_id_seq OWNER TO raven_user;

--
-- Name: frame_series_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.frame_series_id_seq OWNED BY public.frame_series.id;


--
-- Name: glass_types; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.glass_types (
    id integer NOT NULL,
    glass_name character varying(100) NOT NULL,
    glass_code character varying(20) NOT NULL,
    thickness_mm numeric(5,2),
    u_factor numeric(5,3),
    shgc numeric(5,3),
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.glass_types OWNER TO raven_user;

--
-- Name: TABLE glass_types; Type: COMMENT; Schema: public; Owner: raven_user
--

COMMENT ON TABLE public.glass_types IS 'Reference data for glass specifications';


--
-- Name: glass_types_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.glass_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.glass_types_id_seq OWNER TO raven_user;

--
-- Name: glass_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.glass_types_id_seq OWNED BY public.glass_types.id;


--
-- Name: hardware_options; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.hardware_options (
    id integer NOT NULL,
    hardware_name character varying(100) NOT NULL,
    hardware_type character varying(50) NOT NULL,
    manufacturer character varying(100),
    model_number character varying(50),
    finish character varying(50),
    applicable_configs text[],
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.hardware_options OWNER TO raven_user;

--
-- Name: TABLE hardware_options; Type: COMMENT; Schema: public; Owner: raven_user
--

COMMENT ON TABLE public.hardware_options IS 'Reference data for hardware options (locks, handles, hinges)';


--
-- Name: hardware_options_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.hardware_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hardware_options_id_seq OWNER TO raven_user;

--
-- Name: hardware_options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.hardware_options_id_seq OWNED BY public.hardware_options.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    project_name character varying(255) NOT NULL,
    po_number character varying(100),
    customer_name character varying(255),
    billing_address text,
    shipping_address text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.projects OWNER TO raven_user;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_id_seq OWNER TO raven_user;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: windows; Type: TABLE; Schema: public; Owner: raven_user
--

CREATE TABLE public.windows (
    id integer NOT NULL,
    project_id integer,
    item_number character varying(50) NOT NULL,
    room character varying(100),
    width_inches numeric(10,2),
    height_inches numeric(10,2),
    window_type character varying(50),
    frame_series character varying(20),
    swing_direction character varying(20),
    quantity integer,
    frame_color character varying(50),
    glass_type character varying(100),
    grids character varying(50),
    screen character varying(50),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.windows OWNER TO raven_user;

--
-- Name: windows_id_seq; Type: SEQUENCE; Schema: public; Owner: raven_user
--

CREATE SEQUENCE public.windows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.windows_id_seq OWNER TO raven_user;

--
-- Name: windows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raven_user
--

ALTER SEQUENCE public.windows_id_seq OWNED BY public.windows.id;


--
-- Name: configuration_types id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.configuration_types ALTER COLUMN id SET DEFAULT nextval('public.configuration_types_id_seq'::regclass);


--
-- Name: doors id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.doors ALTER COLUMN id SET DEFAULT nextval('public.doors_id_seq'::regclass);


--
-- Name: frame_colors id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_colors ALTER COLUMN id SET DEFAULT nextval('public.frame_colors_id_seq'::regclass);


--
-- Name: frame_series id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_series ALTER COLUMN id SET DEFAULT nextval('public.frame_series_id_seq'::regclass);


--
-- Name: glass_types id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.glass_types ALTER COLUMN id SET DEFAULT nextval('public.glass_types_id_seq'::regclass);


--
-- Name: hardware_options id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.hardware_options ALTER COLUMN id SET DEFAULT nextval('public.hardware_options_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: windows id; Type: DEFAULT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.windows ALTER COLUMN id SET DEFAULT nextval('public.windows_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: configuration_types; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.configuration_types (id, config_name, config_code, panel_count, operable_panels, panel_indicator_style, requires_mullions, requires_hardware, description, created_at) FROM stdin;
1	Fixed	FX	1	0	text_F_centered	f	f	Non-operable fixed window	2025-12-25 00:03:30.225495
2	Single Casement	CS	1	1	diagonal_line	f	t	Single operable casement window - left or right swing	2025-12-25 00:03:30.225495
3	Double Casement	DCS	2	2	diagonal_line	t	t	Two operable casement panels with center mullion	2025-12-25 00:03:30.225495
4	Awning	AW	1	1	horizontal_pivot	f	t	Top-hinged outward opening window	2025-12-25 00:03:30.225495
5	Hopper	HP	1	1	horizontal_pivot_bottom	f	t	Bottom-hinged inward opening window	2025-12-25 00:03:30.225495
6	Slider 2-Panel	SL2	2	1	arrows	t	t	Two-panel horizontal slider - one fixed, one operable	2025-12-25 00:03:30.225495
7	Slider 3-Panel	SL3	3	1	arrows	t	t	Three-panel slider - X-O-X configuration	2025-12-25 00:03:30.225495
8	Slider 4-Panel	SL4	4	2	arrows	t	t	Four-panel slider - X-O-O-X configuration	2025-12-25 00:03:30.225495
9	Pivot	PV	1	1	center_pivot	f	t	Center-pivoting window	2025-12-25 00:03:30.225495
10	Bifold	BF	2	2	bifold_icon	t	t	Bifold door - two panels folding	2025-12-25 00:03:30.225495
11	Accordion	AC	4	4	accordion_icon	t	t	Multi-panel accordion/folding door	2025-12-25 00:03:30.225495
12	Sliding Door 2-Panel	SD2	2	1	arrows	t	t	Patio door - two panels, one operable	2025-12-25 00:03:30.225495
13	Sliding Door 3-Panel	SD3	3	2	arrows	t	t	Patio door - three panels, center operable	2025-12-25 00:03:30.225495
\.


--
-- Data for Name: doors; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.doors (id, project_id, item_number, room, width_inches, height_inches, door_type, frame_series, swing_direction, quantity, frame_color, glass_type, threshold, sill_pan_depth, sill_pan_length, created_at) FROM stdin;
\.


--
-- Data for Name: frame_colors; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.frame_colors (id, color_name, color_code, hex_value, rgb_value, finish_type, created_at) FROM stdin;
1	White	WHT	#FFFFFF	255,255,255	Powder Coat	2025-12-25 00:05:39.561005
2	Bronze	BRZ	#614E1A	97,78,26	Anodized	2025-12-25 00:05:39.561005
3	Black	BLK	#000000	0,0,0	Powder Coat	2025-12-25 00:05:39.561005
4	Silver	SLV	#C0C0C0	192,192,192	Anodized	2025-12-25 00:05:39.561005
5	Beige/Tan	BGE	#D2B48C	210,180,140	Powder Coat	2025-12-25 00:05:39.561005
6	Gray	GRY	#808080	128,128,128	Powder Coat	2025-12-25 00:05:39.561005
7	Dark Bronze	DBR	#3E2723	62,39,35	Anodized	2025-12-25 00:05:39.561005
8	Champagne	CHP	#F7E7CE	247,231,206	Anodized	2025-12-25 00:05:39.561005
9	Custom Color	CUS	\N	\N	Custom Match	2025-12-25 00:05:39.561005
\.


--
-- Data for Name: frame_series; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.frame_series (id, series_name, series_code, frame_width_mm, sash_width_mm, nail_fin_width_mm, nail_fin_height_mm, thermal_break, glass_pocket_depth_mm, description, created_at) FROM stdin;
1	Series 80	80	80.00	40.00	30.00	30.00	t	25.00	Standard fixed window frame - aluminum with thermal break	2025-12-25 00:03:30.217518
2	Series 86	86	86.00	48.00	30.00	30.00	t	28.00	Casement/awning frame - operable windows with multi-point locks	2025-12-25 00:03:30.217518
3	Series 135	135	135.00	65.00	30.00	30.00	t	35.00	Heavy-duty patio door frame - commercial grade	2025-12-25 00:03:30.217518
4	Series 90	90	90.00	45.00	30.00	30.00	t	26.00	Slider frame - horizontal sliding windows	2025-12-25 00:03:30.217518
5	Series 200	200	200.00	80.00	40.00	40.00	t	40.00	Commercial storefront door - heavy-duty	2025-12-25 00:03:30.217518
\.


--
-- Data for Name: glass_types; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.glass_types (id, glass_name, glass_code, thickness_mm, u_factor, shgc, description, created_at) FROM stdin;
1	Single Pane Clear	SPC	3.00	1.040	0.860	Single 1/8" clear glass	2025-12-25 00:05:39.549532
2	Dual Pane Clear	DPC	25.00	0.480	0.700	1" insulated unit - 2 panes clear glass with air gap	2025-12-25 00:05:39.549532
3	Low-E Dual Pane	LED	25.00	0.290	0.560	1" insulated unit - Low-E coating, argon fill	2025-12-25 00:05:39.549532
4	Low-E Triple Pane	LET	38.00	0.200	0.470	1.5" insulated unit - 3 panes with Low-E, argon fill	2025-12-25 00:05:39.549532
5	Tempered Clear	TC	6.00	1.040	0.840	Tempered safety glass - 1/4" thick	2025-12-25 00:05:39.549532
6	Laminated Safety	LS	6.35	0.900	0.750	Laminated safety glass with PVB interlayer	2025-12-25 00:05:39.549532
7	Obscure/Frosted	OF	6.00	1.040	0.780	Privacy glass - textured or frosted	2025-12-25 00:05:39.549532
8	Tinted Bronze	TB	6.00	0.980	0.640	Bronze tinted glass - heat reduction	2025-12-25 00:05:39.549532
9	Impact Resistant	IR	9.00	0.550	0.620	Hurricane impact resistant - laminated dual pane	2025-12-25 00:05:39.549532
\.


--
-- Data for Name: hardware_options; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.hardware_options (id, hardware_name, hardware_type, manufacturer, model_number, finish, applicable_configs, description, created_at) FROM stdin;
1	Standard Casement Lock	Lock	Truth Hardware	T2000	White	{CS,DCS,AW}	Multi-point casement lock with keeper	2025-12-25 00:05:07.448547
2	Heavy-Duty Casement Lock	Lock	Truth Hardware	T3000	Bronze	{CS,DCS}	Commercial grade multi-point lock	2025-12-25 00:05:07.448547
3	Sliding Door Lock	Lock	Ashland Hardware	SDL-100	Satin Nickel	{SD2,SD3}	Mortise lock for sliding patio doors	2025-12-25 00:05:07.448547
4	Slider Window Lock	Lock	Prime-Line	SWL-50	White	{SL2,SL3,SL4}	Cam-action sliding window lock	2025-12-25 00:05:07.448547
5	Casement Operator	Operator	Truth Hardware	CO-200	White	{CS,DCS}	Fold-down handle casement operator	2025-12-25 00:05:07.448547
6	Awning Operator	Operator	Truth Hardware	AO-150	White	{AW}	Push-bar awning window operator	2025-12-25 00:05:07.448547
7	Bifold Hardware Set	Hardware Set	Johnson Hardware	BF-2000	Aluminum	{BF}	Complete bifold door hardware kit - hinges, track, handle	2025-12-25 00:05:07.448547
8	Accordion Track System	Track System	National Guard	AC-500	Bronze	{AC}	Heavy-duty accordion door track and carriers	2025-12-25 00:05:07.448547
9	Door Handle Set	Handle	Ashland Hardware	DH-300	Satin Nickel	{SD2,SD3}	Interior/exterior patio door handle set	2025-12-25 00:05:07.448547
10	Hinges - Casement	Hinge	Truth Hardware	H-400	Stainless	{CS,DCS,AW}	Concealed casement window hinges - set of 2	2025-12-25 00:05:07.448547
11	Hinges - Awning	Hinge	Truth Hardware	H-350	Stainless	{AW,HP}	Top-hung awning hinges	2025-12-25 00:05:07.448547
12	Multipoint Lock Kit	Lock Kit	Truth Hardware	MPL-500	White	{CS,DCS}	Complete multi-point lock system with 3 locking points	2025-12-25 00:05:07.448547
13	Standard Casement Lock	Lock	Truth Hardware	T2000	White	{CS,DCS,AW}	Multi-point casement lock with keeper	2025-12-25 00:05:39.555724
14	Heavy-Duty Casement Lock	Lock	Truth Hardware	T3000	Bronze	{CS,DCS}	Commercial grade multi-point lock	2025-12-25 00:05:39.555724
15	Sliding Door Lock	Lock	Ashland Hardware	SDL-100	Satin Nickel	{SD2,SD3}	Mortise lock for sliding patio doors	2025-12-25 00:05:39.555724
16	Slider Window Lock	Lock	Prime-Line	SWL-50	White	{SL2,SL3,SL4}	Cam-action sliding window lock	2025-12-25 00:05:39.555724
17	Casement Operator	Operator	Truth Hardware	CO-200	White	{CS,DCS}	Fold-down handle casement operator	2025-12-25 00:05:39.555724
18	Awning Operator	Operator	Truth Hardware	AO-150	White	{AW}	Push-bar awning window operator	2025-12-25 00:05:39.555724
19	Bifold Hardware Set	Hardware Set	Johnson Hardware	BF-2000	Aluminum	{BF}	Complete bifold door hardware kit - hinges, track, handle	2025-12-25 00:05:39.555724
20	Accordion Track System	Track System	National Guard	AC-500	Bronze	{AC}	Heavy-duty accordion door track and carriers	2025-12-25 00:05:39.555724
21	Door Handle Set	Handle	Ashland Hardware	DH-300	Satin Nickel	{SD2,SD3}	Interior/exterior patio door handle set	2025-12-25 00:05:39.555724
22	Hinges - Casement	Hinge	Truth Hardware	H-400	Stainless	{CS,DCS,AW}	Concealed casement window hinges - set of 2	2025-12-25 00:05:39.555724
23	Hinges - Awning	Hinge	Truth Hardware	H-350	Stainless	{AW,HP}	Top-hung awning hinges	2025-12-25 00:05:39.555724
24	Multipoint Lock Kit	Lock Kit	Truth Hardware	MPL-500	White	{CS,DCS}	Complete multi-point lock system with 3 locking points	2025-12-25 00:05:39.555724
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.projects (id, project_name, po_number, customer_name, billing_address, shipping_address, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: windows; Type: TABLE DATA; Schema: public; Owner: raven_user
--

COPY public.windows (id, project_id, item_number, room, width_inches, height_inches, window_type, frame_series, swing_direction, quantity, frame_color, glass_type, grids, screen, created_at) FROM stdin;
\.


--
-- Name: configuration_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.configuration_types_id_seq', 59, true);


--
-- Name: doors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.doors_id_seq', 1, false);


--
-- Name: frame_colors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.frame_colors_id_seq', 9, true);


--
-- Name: frame_series_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.frame_series_id_seq', 43, true);


--
-- Name: glass_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.glass_types_id_seq', 9, true);


--
-- Name: hardware_options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.hardware_options_id_seq', 24, true);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.projects_id_seq', 1, false);


--
-- Name: windows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raven_user
--

SELECT pg_catalog.setval('public.windows_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: configuration_types configuration_types_config_name_key; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.configuration_types
    ADD CONSTRAINT configuration_types_config_name_key UNIQUE (config_name);


--
-- Name: configuration_types configuration_types_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.configuration_types
    ADD CONSTRAINT configuration_types_pkey PRIMARY KEY (id);


--
-- Name: doors doors_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.doors
    ADD CONSTRAINT doors_pkey PRIMARY KEY (id);


--
-- Name: frame_colors frame_colors_color_name_key; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_colors
    ADD CONSTRAINT frame_colors_color_name_key UNIQUE (color_name);


--
-- Name: frame_colors frame_colors_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_colors
    ADD CONSTRAINT frame_colors_pkey PRIMARY KEY (id);


--
-- Name: frame_series frame_series_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_series
    ADD CONSTRAINT frame_series_pkey PRIMARY KEY (id);


--
-- Name: frame_series frame_series_series_code_key; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_series
    ADD CONSTRAINT frame_series_series_code_key UNIQUE (series_code);


--
-- Name: frame_series frame_series_series_name_key; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.frame_series
    ADD CONSTRAINT frame_series_series_name_key UNIQUE (series_name);


--
-- Name: glass_types glass_types_glass_name_key; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.glass_types
    ADD CONSTRAINT glass_types_glass_name_key UNIQUE (glass_name);


--
-- Name: glass_types glass_types_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.glass_types
    ADD CONSTRAINT glass_types_pkey PRIMARY KEY (id);


--
-- Name: hardware_options hardware_options_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.hardware_options
    ADD CONSTRAINT hardware_options_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: windows windows_pkey; Type: CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.windows
    ADD CONSTRAINT windows_pkey PRIMARY KEY (id);


--
-- Name: idx_config_types_code; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX idx_config_types_code ON public.configuration_types USING btree (config_code);


--
-- Name: idx_frame_colors_code; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX idx_frame_colors_code ON public.frame_colors USING btree (color_code);


--
-- Name: idx_frame_series_code; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX idx_frame_series_code ON public.frame_series USING btree (series_code);


--
-- Name: idx_glass_types_code; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX idx_glass_types_code ON public.glass_types USING btree (glass_code);


--
-- Name: idx_hardware_type; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX idx_hardware_type ON public.hardware_options USING btree (hardware_type);


--
-- Name: ix_doors_id; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX ix_doors_id ON public.doors USING btree (id);


--
-- Name: ix_projects_id; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX ix_projects_id ON public.projects USING btree (id);


--
-- Name: ix_windows_id; Type: INDEX; Schema: public; Owner: raven_user
--

CREATE INDEX ix_windows_id ON public.windows USING btree (id);


--
-- Name: doors doors_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.doors
    ADD CONSTRAINT doors_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: windows windows_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: raven_user
--

ALTER TABLE ONLY public.windows
    ADD CONSTRAINT windows_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- PostgreSQL database dump complete
--

\unrestrict oELYTukfHwkq9KydPldrkCkPGxwfF8x5G7dIXUnoG6UdrNE0rhAmMrH1wNtLHc1

