

\connect user_db
TRUNCATE TABLE users RESTART IDENTITY CASCADE;
INSERT INTO users (id, name, email, hashed_password) VALUES
  (1, 'Ali Rezaei', 'ali@example.com', '$2b$12$ByQPzfcZ60hyW4uUlaLuk.fKbVFF6bFkotShICY0EAtpEqbKzeS.S'),
  (2, 'Sara Ahmadi', 'sara@example.com', '$2b$12$ByQPzfcZ60hyW4uUlaLuk.fKbVFF6bFkotShICY0EAtpEqbKzeS.S'),
  (3, 'Demo Admin', 'admin@example.com', '$2b$12$ByQPzfcZ60hyW4uUlaLuk.fKbVFF6bFkotShICY0EAtpEqbKzeS.S');
SELECT setval(pg_get_serial_sequence('users','id'), 3, true);

\connect product_db
TRUNCATE TABLE products RESTART IDENTITY CASCADE;
INSERT INTO products (id, name, price, description) VALUES
  (1, 'Mechanical Keyboard', 89.99, 'Compact RGB mechanical keyboard for developers'),
  (2, 'USB-C Hub', 39.50, '7-in-1 USB-C hub with HDMI and Ethernet'),
  (3, 'Noise Cancelling Headphones', 129.00, 'Wireless headphones for focus work'),
  (4, 'Laptop Stand', 34.75, 'Aluminium ergonomic laptop stand'),
  (5, 'Portable SSD 1TB', 94.90, 'Fast external SSD for backups and projects');
SELECT setval(pg_get_serial_sequence('products','id'), 5, true);

\connect order_db
TRUNCATE TABLE outbox_events RESTART IDENTITY CASCADE;
TRUNCATE TABLE orders RESTART IDENTITY CASCADE;
INSERT INTO orders (id, user_id, product_id, quantity, total_price, status, created_at) VALUES
  (1, 1, 1, 1, 89.99, 'pending', now() - interval '3 days'),
  (2, 1, 2, 2, 79.00, 'pending', now() - interval '2 days'),
  (3, 2, 3, 1, 129.00, 'pending', now() - interval '1 day'),
  (4, 3, 5, 1, 94.90, 'pending', now());
INSERT INTO outbox_events (id, aggregate_type, aggregate_id, event_type, payload, published, created_at) VALUES
  (1, 'Order', 1, 'OrderCreated', '{"id":1,"user_id":1,"product_id":1,"quantity":1,"total_price":89.99}', true, now() - interval '3 days'),
  (2, 'Order', 2, 'OrderCreated', '{"id":2,"user_id":1,"product_id":2,"quantity":2,"total_price":79.0}', true, now() - interval '2 days'),
  (3, 'Order', 3, 'OrderCreated', '{"id":3,"user_id":2,"product_id":3,"quantity":1,"total_price":129.0}', false, now() - interval '1 day'),
  (4, 'Order', 4, 'OrderCreated', '{"id":4,"user_id":3,"product_id":5,"quantity":1,"total_price":94.9}', false, now());
SELECT setval(pg_get_serial_sequence('orders','id'), 4, true);
SELECT setval(pg_get_serial_sequence('outbox_events','id'), 4, true);

\connect payment_db
TRUNCATE TABLE payments RESTART IDENTITY CASCADE;
INSERT INTO payments (id, order_id, amount, currency, status, created_at) VALUES
  ('pay_demo_001', '1', 89.99, 'USD', 'authorized', now() - interval '3 days'),
  ('pay_demo_002', '2', 79.00, 'USD', 'authorized', now() - interval '2 days'),
  ('pay_demo_003', '3', 129.00, 'USD', 'failed', now() - interval '1 day'),
  ('pay_demo_004', '4', 94.90, 'USD', 'pending', now());

-- \connect notification_db
-- -- notification-service currently only has processed_events
-- TRUNCATE TABLE processed_events RESTART IDENTITY CASCADE;
-- INSERT INTO processed_events (id, event_id, processed_at) VALUES
--   (1, 'OrderCreated:1', now() - interval '3 days'),
--   (2, 'PaymentAuthorized:pay_demo_001', now() - interval '3 days'),
--   (3, 'PaymentAuthorized:pay_demo_002', now() - interval '2 days'),
--   (4, 'PaymentFailed:pay_demo_003', now() - interval '1 day');
-- SELECT setval(pg_get_serial_sequence('processed_events','id'), 4, true);