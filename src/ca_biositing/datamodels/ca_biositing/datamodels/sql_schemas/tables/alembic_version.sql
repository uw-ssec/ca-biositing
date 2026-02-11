--
-- Name: alembic_version; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS alembic_version (
    version_num varchar(32),
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
