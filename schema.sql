CREATE TABLE public.article_group (
    article_id integer,
    group_id integer
);


CREATE TABLE public.articles (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    author character varying(255),
    written date,
    creator integer NOT NULL,
    content text NOT NULL,
    hidden boolean,
    url text
);


CREATE SEQUENCE public.article_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.article_id_seq OWNED BY public.articles.id;


CREATE TABLE public.article_topic (
    article_id integer,
    topic_id integer
);


CREATE TABLE public.comments (
    id integer NOT NULL,
    article_id integer,
    name character varying(255)
);


CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


CREATE TABLE public.interest_groups (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


CREATE SEQUENCE public.interest_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.interest_group_id_seq OWNED BY public.interest_groups.id;


CREATE TABLE public.topics (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


CREATE SEQUENCE public.topic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.topic_id_seq OWNED BY public.topics.id;


CREATE TABLE public.user_group (
    user_id integer,
    group_id integer
);


CREATE TABLE public.user_topic (
    user_id integer,
    topic_id integer
);


CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


ALTER TABLE ONLY public.articles ALTER COLUMN id SET DEFAULT nextval('public.article_id_seq'::regclass);


ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


ALTER TABLE ONLY public.interest_groups ALTER COLUMN id SET DEFAULT nextval('public.interest_group_id_seq'::regclass);


ALTER TABLE ONLY public.topics ALTER COLUMN id SET DEFAULT nextval('public.topic_id_seq'::regclass);


ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


ALTER TABLE ONLY public.articles
    ADD CONSTRAINT article_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.interest_groups
    ADD CONSTRAINT interest_group_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topic_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT unique_username UNIQUE (username);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.article_group
    ADD CONSTRAINT article_group_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.articles(id);


ALTER TABLE ONLY public.article_group
    ADD CONSTRAINT article_group_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


ALTER TABLE ONLY public.article_topic
    ADD CONSTRAINT article_topic_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.articles(id);


ALTER TABLE ONLY public.article_topic
    ADD CONSTRAINT article_topic_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(id);


ALTER TABLE ONLY public.articles
    ADD CONSTRAINT articles_creator_fkey FOREIGN KEY (creator) REFERENCES public.users(id);


ALTER TABLE ONLY public.comments
    ADD CONSTRAINT fk_article FOREIGN KEY (article_id) REFERENCES public.articles(id);


ALTER TABLE ONLY public.user_group
    ADD CONSTRAINT user_group_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


ALTER TABLE ONLY public.user_group
    ADD CONSTRAINT user_group_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


ALTER TABLE ONLY public.user_topic
    ADD CONSTRAINT user_topic_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(id);


ALTER TABLE ONLY public.user_topic
    ADD CONSTRAINT user_topic_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

