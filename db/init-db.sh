set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE rottenpotatoes;
    GRANT ALL PRIVILEGES ON DATABASE rottenpotatoes TO docker;
EOSQL

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "rottenpotatoes" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    DROP TABLE IF EXISTS users CASCADE;
    DROP TABLE IF EXISTS profile CASCADE;
    DROP TABLE IF EXISTS games CASCADE;
    DROP TABLE IF EXISTS reviews CASCADE;
    DROP TABLE IF EXISTS comments CASCADE;
    DROP TABLE IF EXISTS likes CASCADE;

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
    (uuid_generate_v4(), 'bob', 'scrypt:32768:8:1\$SBi6YshE5Wni1VjF\$9967d23e2ce69770177a090f171f4023fbc38b93d45a924a43fa48dd762e8d9e9105f151ded2fd1e0abf691809da51ca107c88c495b2179bcd6fd0e1cad5f83a', TRUE),
    (uuid_generate_v4(), 'alice', 'scrypt:32768:8:1\$XTOzBi61QOkjhK8h\$b8490c1fc30921bd65947b5f51259977911fcda0e989c5184f37dce5046c86b382c4451f0719fa49642396a973014268cfcd5c54b12eb9e67117fff8819df856', TRUE),
    (uuid_generate_v4(), 'patrick', 'scrypt:32768:8:1\$mUhOpKzKRHlV3w8k\$ea3a3a6a730d6ad4257c09968f0114b56c677d12b86b5aab2190945606ddbdc9b969c4a6d7ab58cd567cd76776f5e3dea4b4b95b65256163a4f6be31660fa5ab', TRUE);
EOSQL
