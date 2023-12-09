-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR (255),
    balance DECIMAL(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE Seller(
    uid INT NOT NULL PRIMARY KEY REFERENCES Users(id)
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    product_id INT NOT NULL,
    sid INT NOT NULL REFERENCES Seller(uid),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    description VARCHAR(1020) NOT NULL, 
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Orders (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    order_fulfilled BOOLEAN NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    total_price DECIMAL(12,2) NOT NULL
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    oid INT NOT NULL REFERENCES Orders(id),
    qty INT NOT NULL,
    purchase_fulfilled BOOLEAN NOT NULL,
    time_fulfilled timestamp without time zone NULL,
    sid INT NOT NULL REFERENCES Seller(uid),
    unit_price DECIMAL(12,2) NOT NULL
);

CREATE TABLE Wishes (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Reviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_posted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'), 
    rating DECIMAL(1,0) NOT NULL CHECK (rating >=1 AND rating <= 5), 
    review_text VARCHAR(500)
 );

 CREATE TABLE SellerReviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id), --user that writes the review
    sid INT NOT NULL REFERENCES Seller(uid), --seller that recieves the review
    time_posted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'), 
    rating DECIMAL(1,0) NOT NULL CHECK (rating >=1 AND rating <= 5), 
    review_text VARCHAR(500)
 );
 
CREATE TABLE Inventory (
    id INT NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    sid INT NOT NULL REFERENCES Seller(uid), -- uid of a seller/merchant
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL, --available quantity
    PRIMARY KEY(sid, pid)
);

CREATE TABLE Cart (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    qty INT NOT NULL,
    PRIMARY KEY(uid, pid)
);