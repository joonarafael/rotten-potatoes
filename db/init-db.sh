set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE rottenpotatoes;
    GRANT ALL PRIVILEGES ON DATABASE rottenpotatoes TO docker;
EOSQL

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "rottenpotatoes" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- User tables

    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        is_admin BOOL NOT NULL DEFAULT FALSE
    );

    CREATE TABLE genres (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL UNIQUE
    );

    CREATE TABLE movies (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        title VARCHAR(255) NOT NULL UNIQUE,
        description VARCHAR(1250) NOT NULL,
        year INT NOT NULL,
        genre_id UUID REFERENCES genres(id) ON DELETE CASCADE NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

    CREATE TABLE likes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        movie_id UUID REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
        rating INT NOT NULL
    );

    CREATE TABLE reviews (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        movie_id UUID REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
        review VARCHAR(1250) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

    -- use \$\$ to escape shell expansion

    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS \$\$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    \$\$ LANGUAGE plpgsql;

    CREATE TRIGGER set_updated_at_users
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

    CREATE TRIGGER set_updated_at_movies
    BEFORE UPDATE ON movies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

    CREATE TRIGGER set_updated_at_reviews
    BEFORE UPDATE ON reviews
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

    INSERT INTO users (id, username, password, is_admin)
    VALUES
    (uuid_generate_v4(), 'bob', 'squarepants', TRUE),
    (uuid_generate_v4(), 'alice', 'redqueen', TRUE),
    (uuid_generate_v4(), 'patrick', 'asteroid', TRUE);
EOSQL
