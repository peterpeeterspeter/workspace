-- Supabase Import for Sawiday Products
-- Generated: 2026-02-13T12:46:25.118398
-- Total products: 102
-- Source: Sawiday scraper

-- Category Mappings (Dutch → English):
-- Baden → Bathtub
-- Douche → Shower
-- Kranen → Faucet
-- Toiletten → Toilet
-- Wastafels → Vanity
-- Spiegels → Lighting

-- Price Tier Cutoffs (per category):
-- baden:
--   budget: €266.57
--   economy: €379.00
--   premium: €682.05
--   luxury: €1006.72

-- nl-be:
--   budget: €179.45
--   economy: €309.99
--   premium: €486.99
--   luxury: €899.00

-- douche:
--   budget: €149.99
--   economy: €279.99
--   premium: €507.99
--   luxury: €551.99

-- kranen:
--   budget: €149.99
--   economy: €239.99
--   premium: €499.99
--   luxury: €649.99

-- Adema:
--   budget: €116.99
--   economy: €152.99
--   premium: €161.99
--   luxury: €216.99

-- Saniclass:
--   budget: €89.99
--   economy: €104.99
--   premium: €169.99
--   luxury: €412.99

-- Smedbo:
--   budget: €134.99
--   economy: €134.99
--   premium: €134.99
--   luxury: €134.99

BEGIN;

INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit D-code inbouwbad',
  'Duravit',
  266.57,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/76009950/duravit-d-code-kunststof-bad-acryl-rechthoekig-160x70x40cm-zonder-poten-wit',
  'https://static.rorix.nl/image/product/galvano/2000x2000/40b03c2f0b970fb8d7d4ed1930e7a100.jpg/duravit-d-code-bad-acryl-rechthoekig-160x70x40cm-wit-0297511.jpg',
  '["https://static.rorix.nl/image/product/galvano/2000x2000/40b03c2f0b970fb8d7d4ed1930e7a100.jpg/duravit-d-code-bad-acryl-rechthoekig-160x70x40cm-wit-0297511.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a6fdc7e2fe2d8520f261450c8838561f.jpg/duravit-d-code-bad-acryl-rechthoekig-160x70x40cm-wit-0297511.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/457c4eabf5cc565c36fc739eb47aaa04.jpg/duravit-d-code-bad-acryl-rechthoekig-160x70x40cm-wit-0297511.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001439326.jpg/duravit-d-code-bad-acryl-rechthoekig-160x70x40cm-wit-0297511.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001440110.jpg/duravit-d-code-bad-acryl-rechthoekig-160x70x40cm-wit-0297511.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit D-code inbouwbad',
  'Duravit',
  405.44,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/76009955/duravit-d-code-bad-rechthoek-180x80cm-duo-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/245578b2f8bead3a5aadd9823d369809.jpg/duravit-d-code-bad-rechthoek-180x80cm-duo-wit-0297516.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/245578b2f8bead3a5aadd9823d369809.jpg/duravit-d-code-bad-rechthoek-180x80cm-duo-wit-0297516.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e4bf242a29565983eac7a7a5d6998f8f.jpg/duravit-d-code-bad-rechthoek-180x80cm-duo-wit-0297516.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001212332.jpg/duravit-d-code-bad-rechthoek-180x80cm-duo-wit-0297516.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/dfdb3bc50f2f6d68ca6b4a3b57543973.jpg/duravit-d-code-bad-rechthoek-180x80cm-duo-wit-0297516.jpg", "https://static.rorix.nl/document/product/galvano/D130001001327155.gif"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit D-code inbouwbad',
  'Duravit',
  288.2,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/76009952/duravit-d-code-kunststof-bad-acryl-rechthoekig-170x70x40cm-zonder-poten-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/c67ed7218c396aa29c3b208c9a549ced.jpg/duravit-d-code-bad-acryl-rechthoekig-170x70x40cm-wit-0297513.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c67ed7218c396aa29c3b208c9a549ced.jpg/duravit-d-code-bad-acryl-rechthoekig-170x70x40cm-wit-0297513.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8e9839a8ff961ac8396c66992cbb1ea1.jpg/duravit-d-code-bad-acryl-rechthoekig-170x70x40cm-wit-0297513.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f44f2f529ed3332a7ddcc83496587084.jpg/duravit-d-code-bad-acryl-rechthoekig-170x70x40cm-wit-0297513.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001212326.jpg/duravit-d-code-bad-acryl-rechthoekig-170x70x40cm-wit-0297513.jpg", "https://static.rorix.nl/document/product/galvano/D130001001327067.gif"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch Oberon inbouwbad',
  'Villeroy & Boch',
  682.05,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/16166/villeroy-en-boch-oberon-bad-170x70cm-quaryl-rechthoekig-met-poten-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/9d1a50943c8fc71590ee2c8a95af40bf.jpg/villeroy-boch-oberon-bad-170x70cm-quaryl-rechthoekig-met-poten-wit-0949984.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/9d1a50943c8fc71590ee2c8a95af40bf.jpg/villeroy-boch-oberon-bad-170x70cm-quaryl-rechthoekig-met-poten-wit-0949984.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001264042.jpg/villeroy-boch-oberon-bad-170x70cm-quaryl-rechthoekig-met-poten-wit-0949984.jpg", "https://static.rorix.nl/document/product/galvano/D130001001264040.jpg", "https://static.rorix.nl/document/product/overig/cc4a6362a6be61e6c86061fbe12cec5e.png", "https://static.rorix.nl/document/product/overig/40c7a469aa07af533d49e2c0a127d891.png"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch O.novo Design Duobad',
  'Villeroy & Boch',
  379.0,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/75630288/villeroy-en-boch-o.novo-design-kunststof-bad-acryl-rechthoekig-180x80x48cm-exclusief-poten-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/4c30efceb793e54a1d15bc4da09cb468.jpg/villeroy-boch-o.novo-design-bad-acryl-rechthoekig-180x80x48cm-wit-0930450.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/4c30efceb793e54a1d15bc4da09cb468.jpg/villeroy-boch-o.novo-design-bad-acryl-rechthoekig-180x80x48cm-wit-0930450.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6d73244f49b12d89e27ccfd35248e3f6.jpg/villeroy-boch-o.novo-design-bad-acryl-rechthoekig-180x80x48cm-wit-0930450.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001264014.jpeg/villeroy-boch-o.novo-design-bad-acryl-rechthoekig-180x80x48cm-wit-0930450.jpeg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/c5a00e0b846e8fca49b45b512c76c0b2.jpg/villeroy-boch-o.novo-design-bad-acryl-rechthoekig-180x80x48cm-wit-0930450.jpg", "https://static.rorix.nl/document/product/galvano/D130001001264012.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch Architectura inbouwbad',
  'Villeroy & Boch',
  410.77,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/75670406/villeroy-en-boch-omnia-architectura-bad-150x70-cm.-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/4cd2206b1adca4f438e5149834ad2c70.jpg/villeroy-boch-omnia-architectura-bad-150x70cm-wit-ga68304.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/4cd2206b1adca4f438e5149834ad2c70.jpg/villeroy-boch-omnia-architectura-bad-150x70cm-wit-ga68304.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/75538ebd6678feae42c9b070955b2494.jpg/villeroy-boch-omnia-architectura-bad-150x70cm-wit-ga68304.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0dc18f60a307c59c59d8323833569011.jpg/villeroy-boch-omnia-architectura-bad-150x70cm-wit-ga68304.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001263735.jpg/villeroy-boch-omnia-architectura-bad-150x70cm-wit-ga68304.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/01a1c3b03183f41de4340a19144d04ec.jpg/villeroy-boch-omnia-architectura-bad-150x70cm-wit-ga68304.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch O.novo inbouwbad',
  'Villeroy & Boch',
  412.67,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/67586/villeroy-boch-o.novo-bad-rechthoek-solo-170x70-cm.-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/3bbbb73b0f4417583bb04ea31f057d9e.jpg/villeroy-boch-o.novo-bad-rechthoek-solo-170x70cm-wit-0930602.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/3bbbb73b0f4417583bb04ea31f057d9e.jpg/villeroy-boch-o.novo-bad-rechthoek-solo-170x70cm-wit-0930602.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/4072e3db394c733f50c6b39bb80cdd3b.jpg/villeroy-boch-o.novo-bad-rechthoek-solo-170x70cm-wit-0930602.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/15b109aaf3fbadcb41fee1f0c11ebb7b.jpg/villeroy-boch-o.novo-bad-rechthoek-solo-170x70cm-wit-0930602.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001264008.jpg/villeroy-boch-o.novo-bad-rechthoek-solo-170x70cm-wit-0930602.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D13000100178229.jpeg/villeroy-boch-o.novo-bad-rechthoek-solo-170x70cm-wit-0930602.jpeg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch Oberon inbouwbad',
  'Villeroy & Boch',
  682.05,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/16169/villeroy-en-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/9d1a50943c8fc71590ee2c8a95af40bf.jpg/villeroy-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit-0944912.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/9d1a50943c8fc71590ee2c8a95af40bf.jpg/villeroy-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit-0944912.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2be026c92f9cf69323cae1707258f4e8.jpg/villeroy-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit-0944912.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5391ae61cf94332c44fed8226e1086b3.jpg/villeroy-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit-0944912.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/68bbe8dbd35c8ea6a67a7ac6fc2de8ba.jpg/villeroy-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit-0944912.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9ddd6f74068e5d84c0eed86084d8f41a.jpg/villeroy-boch-oberon-bad-170x75cm-quaryl-rechthoekig-met-poten-wit-0944912.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'WaveDesign by Wisa Tesa Alle baden',
  'WaveDesign by Wisa',
  673.99,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/76915733/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/dae6d09d9cccfc60693df76e5e0a2a93.jpg/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit-sw115569.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/dae6d09d9cccfc60693df76e5e0a2a93.jpg/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit-sw115569.jpg", "https://static.rorix.nl/image/product/technische-unie/2000x2000/7b8fe3d8f62e1985bec1a96d3f1a860b.jpg/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit-sw115569.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001190618.jpg/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit-sw115569.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001190617.jpg/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit-sw115569.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/dae6d09d9cccfc60693df76e5e0a2a93.jpg/wavedesign-by-wisa-tesa-ligbad-170x80x50cm-52cm-rechthoek-acryl-wit-sw115569.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'WaveDesign by Wisa Amarante inbouwbad',
  'WaveDesign by Wisa',
  589.15,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/76915589/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit',
  'https://static.rorix.nl/image/product/technische-unie/2000x2000/3e58ea0b030b80636a008bc0e047d90d.jpg/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit-sw115425.jpg',
  '["https://static.rorix.nl/image/product/technische-unie/2000x2000/3e58ea0b030b80636a008bc0e047d90d.jpg/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit-sw115425.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001268263.jpg/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit-sw115425.jpg", "https://static.rorix.nl/image/product/technische-unie/2000x2000/3e58ea0b030b80636a008bc0e047d90d.jpg/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit-sw115425.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001268263.jpg/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit-sw115425.jpg", "https://static.rorix.nl/image/product/technische-unie/2000x2000/3e58ea0b030b80636a008bc0e047d90d.jpg/wavedesign-by-wisa-amarante-ligbad-170x75x48cm-met-gat-rechthoek-kunststof-wit-sw115425.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'WaveDesign by Wisa Tesa Alle baden',
  'WaveDesign by Wisa',
  600.99,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/76915734/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/dae6d09d9cccfc60693df76e5e0a2a93.jpg/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit-sw115570.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/dae6d09d9cccfc60693df76e5e0a2a93.jpg/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit-sw115570.jpg", "https://static.rorix.nl/image/product/technische-unie/2000x2000/02994304f2f02f03a51f72977a4b0bce.jpg/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit-sw115570.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001190619.jpg/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit-sw115570.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001190618.jpg/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit-sw115570.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/dae6d09d9cccfc60693df76e5e0a2a93.jpg/wavedesign-by-wisa-tesa-ligbad-180x80cm-rechthoek-acryl-glans-wit-sw115570.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Nemo Start Bad douche combinatie',
  'Nemo',
  319.99,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/77079155/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/3dec732923d71fdefebda8bb4b265a20.jpg/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl-sw294677.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/3dec732923d71fdefebda8bb4b265a20.jpg/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl-sw294677.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2df2640da303c08333fec02fd43bb0fc.jpg/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl-sw294677.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/562cd3104204361c9d45a1973e5113ab.jpg/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl-sw294677.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/3dec732923d71fdefebda8bb4b265a20.jpg/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl-sw294677.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2df2640da303c08333fec02fd43bb0fc.jpg/nemo-start-combi-ii-douchebad-170x75x44cm-210l-met-potenstel-wit-acryl-sw294677.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Nemo Start Bad douche combinatie',
  'Nemo',
  296.99,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/77079259/nemo-start-combi-i-douchebad-mono-afvoer-d52-1800x800x440mm-275l-met-potenstel-wit-acryl-conform-en-normen-en-198-,-en-232-en-14516-2010',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/b9a1e441cebcd755e167a0ea37973700.jpg/nemo-start-combi-i-douchebad-180x80x44cm-275l-met-potenstel-wit-acryl-sw294780.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/b9a1e441cebcd755e167a0ea37973700.jpg/nemo-start-combi-i-douchebad-180x80x44cm-275l-met-potenstel-wit-acryl-sw294780.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2df2640da303c08333fec02fd43bb0fc.jpg/nemo-start-combi-i-douchebad-180x80x44cm-275l-met-potenstel-wit-acryl-sw294780.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/fd9081918ed2232dbb2f972bcbe0fb23.jpg/nemo-start-combi-i-douchebad-180x80x44cm-275l-met-potenstel-wit-acryl-sw294780.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/b9a1e441cebcd755e167a0ea37973700.jpg/nemo-start-combi-i-douchebad-180x80x44cm-275l-met-potenstel-wit-acryl-sw294780.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2df2640da303c08333fec02fd43bb0fc.jpg/nemo-start-combi-i-douchebad-180x80x44cm-275l-met-potenstel-wit-acryl-sw294780.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Nemo Spring inbouwbad',
  'Nemo',
  277.99,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/77079348/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-conform-en-normen-en-198-,-en-232-en-14516-2010',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/fe53045354799646ea04c6794a3850a2.jpg/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-sw294870.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/fe53045354799646ea04c6794a3850a2.jpg/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-sw294870.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/a9ebc319c63e3c3c7984302d78fce15e.jpg/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-sw294870.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/fe53045354799646ea04c6794a3850a2.jpg/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-sw294870.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/a9ebc319c63e3c3c7984302d78fce15e.jpg/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-sw294870.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/fe53045354799646ea04c6794a3850a2.jpg/nemo-spring-nantes-inbouwbad-mono-afvoer-d52-170x75x40cm-185l-met-potenstel-wit-acryl-sw294870.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Nemo Start inbouwbad',
  'Nemo',
  279.99,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/77079275/nemo-start-zen-ii-inbouwbad-mono-afvoer-d52-1700x750x400mm-230l-met-potenstel-wit-acryl-conform-en-normen-en-198-,-en-232-en-14516-2010',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/e3d24c19bef37616845aa418ce1fa789.jpg/nemo-start-zen-ii-inbouwbad-170x75x40cm-230l-met-potenstel-wit-acryl-sw294797.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/e3d24c19bef37616845aa418ce1fa789.jpg/nemo-start-zen-ii-inbouwbad-170x75x40cm-230l-met-potenstel-wit-acryl-sw294797.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/70616ae848b61c45b5cd3e7c6ea8a78c.jpg/nemo-start-zen-ii-inbouwbad-170x75x40cm-230l-met-potenstel-wit-acryl-sw294797.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/31b9fe6f162d536bb1048645aaa57c8d.jpg/nemo-start-zen-ii-inbouwbad-170x75x40cm-230l-met-potenstel-wit-acryl-sw294797.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/953f1c1d2a20d09bb19720219ccb08a5.jpg/nemo-start-zen-ii-inbouwbad-170x75x40cm-230l-met-potenstel-wit-acryl-sw294797.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/e3d24c19bef37616845aa418ce1fa789.jpg/nemo-start-zen-ii-inbouwbad-170x75x40cm-230l-met-potenstel-wit-acryl-sw294797.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Nemo Start inbouwbad',
  'Nemo',
  269.99,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/77079207/nemo-start-zen-i-inbouwbad-mono-afvoer-d52-1700x700x400mm-205l-met-potenstel-wit-acryl-conform-en-normen-en-198-,-en-232-en-14516-2010',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/a4020671932e60af47c39fa79ffa52a0.jpg/nemo-start-zen-i-inbouwbad-170x70x40cm-205-liter-met-potenstel-wit-acryl-sw294728.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/a4020671932e60af47c39fa79ffa52a0.jpg/nemo-start-zen-i-inbouwbad-170x70x40cm-205-liter-met-potenstel-wit-acryl-sw294728.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/b6ad246b2fbfc85d4d5d84f72dfb6ed7.jpg/nemo-start-zen-i-inbouwbad-170x70x40cm-205-liter-met-potenstel-wit-acryl-sw294728.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/a4020671932e60af47c39fa79ffa52a0.jpg/nemo-start-zen-i-inbouwbad-170x70x40cm-205-liter-met-potenstel-wit-acryl-sw294728.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/b6ad246b2fbfc85d4d5d84f72dfb6ed7.jpg/nemo-start-zen-i-inbouwbad-170x70x40cm-205-liter-met-potenstel-wit-acryl-sw294728.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/a4020671932e60af47c39fa79ffa52a0.jpg/nemo-start-zen-i-inbouwbad-170x70x40cm-205-liter-met-potenstel-wit-acryl-sw294728.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Xenz Kanaga inbouwbad',
  'Xenz',
  1057.54,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/76899877/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/73e6b4338dcd0b0c7345dd53b1e1365a.jpg/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit-sw103330.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/73e6b4338dcd0b0c7345dd53b1e1365a.jpg/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit-sw103330.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/432502cf3f566a49d8d3829203a58ca8.jpg/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit-sw103330.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e5ff2ed9d499cdf82411cfd0920cda89.jpg/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit-sw103330.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2c44e9232356391283813d2576231e73.jpg/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit-sw103330.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ad122efec1944a389ba0b57e34e386a7.jpg/xenz-kanaga-duobad-190x90x53-afvoer-midden-acryl-wit-sw103330.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Xenz Kristal inbouwbad',
  'Xenz',
  845.79,
  'baden',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77135578/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/141c7dc4933392028c31dbafaef08788.jpg/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit-sw378483.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/141c7dc4933392028c31dbafaef08788.jpg/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit-sw378483.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/56484eddde523d587b19e9b9ce766899.jpg/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit-sw378483.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7e63a3712c5f891f3756df5e8240d5f9.jpg/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit-sw378483.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7ccc83da9446efab08d2a8473db750ee.jpg/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit-sw378483.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a1366d282920c60b7345ff8578cb2145.jpg/xenz-kristal-ligbad-180x80x48-afvoer-midden-acryl-wit-sw378483.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Xenz Kristal inbouwbad',
  'Xenz',
  1038.18,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77135552/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement',
  'https://static.rorix.nl/image/product/overig/2000x2000/5604ddc23c6914457d9e0b16f9426c7a.jpg/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement-sw378458.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/5604ddc23c6914457d9e0b16f9426c7a.jpg/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement-sw378458.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e06e99594a58bd489c29884ce1cd88c5.jpg/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement-sw378458.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7a046fd341fcdfc935456de36d4bdbea.jpg/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement-sw378458.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7ccc83da9446efab08d2a8473db750ee.jpg/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement-sw378458.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f07fa67a31ca3f1b70ff9b8c84867746.jpg/xenz-kristal-ligbad-170x75x48-afvoer-midden-acryl-cement-sw378458.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Xenz Kristal inbouwbad',
  'Xenz',
  1006.72,
  'baden',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77135526/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony',
  'https://static.rorix.nl/image/product/overig/2000x2000/a6e1d61b522c4f190968b8784c1b6307.jpg/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony-sw378434.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/a6e1d61b522c4f190968b8784c1b6307.jpg/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony-sw378434.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/38b25d3c89cac1abf7322827abd17782.jpg/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony-sw378434.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/1e837921f93c8162b6a46610f62b09d9.jpg/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony-sw378434.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7ccc83da9446efab08d2a8473db750ee.jpg/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony-sw378434.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/05ae52431e6de1b11cdae96c655a067f.jpg/xenz-kristal-ligbad-160x75x48-afvoer-midden-acryl-ebony-sw378434.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Xenz Robijn inbouwbad',
  'Xenz',
  1069.64,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77135390/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat',
  'https://static.rorix.nl/image/product/overig/2000x2000/ad12f2eef9fc1ea24e141fbb15ad4029.jpg/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat-sw378297.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/ad12f2eef9fc1ea24e141fbb15ad4029.jpg/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat-sw378297.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b155661a57595526fbd52795bdd394eb.jpg/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat-sw378297.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d50778a1da551036e828829a09d22586.jpg/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat-sw378297.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/fe794ac42641ecc2126acd33e6b4aafb.jpg/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat-sw378297.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f6ee6a1081cfc359209d4dd9e23fae88.jpg/xenz-robijn-duobad-180x80x48-afvoer-midden-acryl-wit-mat-sw378297.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Zeza Square inbouwbad',
  'Zeza',
  194.99,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77792522/zeza-square-ligbad-180x80cm-acryl-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/ca9fa01710cc8a2c5f6c6228aaf55191.jpg/zeza-square-ligbad-180x80cm-acryl-glans-wit-sw1015084.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/ca9fa01710cc8a2c5f6c6228aaf55191.jpg/zeza-square-ligbad-180x80cm-acryl-glans-wit-sw1015084.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/741e28651f53d78ff19a3c5f1ecbe97c.jpg/zeza-square-ligbad-180x80cm-acryl-glans-wit-sw1015084.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/4074bfd2718c388a98c6d1c7b13afd72.jpg/zeza-square-ligbad-180x80cm-acryl-glans-wit-sw1015084.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/00a8659b49153edf9a86556bd1e4fc2f.jpg/zeza-square-ligbad-180x80cm-acryl-glans-wit-sw1015084.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5e441b36812227d234b0d9cc59298218.jpg/zeza-square-ligbad-180x80cm-acryl-glans-wit-sw1015084.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Zeza Oval inbouwbad',
  'Zeza',
  204.99,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77792518/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/e64483a13e0a3a0cb525ae4aeceb42c4.jpg/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit-sw1015080.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/e64483a13e0a3a0cb525ae4aeceb42c4.jpg/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit-sw1015080.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e8fe10306d380fd1dfe2ecbc46e9297f.jpg/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit-sw1015080.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e29989628db0c387462b0fd4f1127b47.jpg/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit-sw1015080.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7f6f623e167157bf2ad8029919c38f37.jpg/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit-sw1015080.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0f0e990fb1225d2afac326c0f2a961e0.jpg/zeza-oval-ligbad-190x90cm-acryl-duo-glans-wit-sw1015080.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Zeza Oval inbouwbad',
  'Zeza',
  184.99,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77792520/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/e64483a13e0a3a0cb525ae4aeceb42c4.jpg/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit-sw1015082.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/e64483a13e0a3a0cb525ae4aeceb42c4.jpg/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit-sw1015082.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e8fe10306d380fd1dfe2ecbc46e9297f.jpg/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit-sw1015082.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e29989628db0c387462b0fd4f1127b47.jpg/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit-sw1015082.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7f6f623e167157bf2ad8029919c38f37.jpg/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit-sw1015082.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0f0e990fb1225d2afac326c0f2a961e0.jpg/zeza-oval-ligbad-170x70cm-acryl-duo-glans-wit-sw1015082.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Zeza Square inbouwbad',
  'Zeza',
  204.99,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77792519/zeza-square-ligbad-190x90cm-acryl-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/ca9fa01710cc8a2c5f6c6228aaf55191.jpg/zeza-square-ligbad-190x90cm-acryl-glans-wit-sw1015081.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/ca9fa01710cc8a2c5f6c6228aaf55191.jpg/zeza-square-ligbad-190x90cm-acryl-glans-wit-sw1015081.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/741e28651f53d78ff19a3c5f1ecbe97c.jpg/zeza-square-ligbad-190x90cm-acryl-glans-wit-sw1015081.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/4074bfd2718c388a98c6d1c7b13afd72.jpg/zeza-square-ligbad-190x90cm-acryl-glans-wit-sw1015081.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/00a8659b49153edf9a86556bd1e4fc2f.jpg/zeza-square-ligbad-190x90cm-acryl-glans-wit-sw1015081.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5e441b36812227d234b0d9cc59298218.jpg/zeza-square-ligbad-190x90cm-acryl-glans-wit-sw1015081.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke inbouwbad',
  'GO by Van Marcke',
  371.94,
  'baden',
  'economy',
  'https://www.sawiday.be/nl-be/p/77203586/go-by-van-marcke-stelli-inbouwbad-duo-190x90x48cm-230l-wit-acryl-met-potenstel',
  'https://static.rorix.nl/image/product/overig/2000x2000/e98dbc34a136d2baa77465e2b97ec660.jpg/go-by-van-marcke-stelli-inbouwbad-duo-190x90x48cm-230l-wit-acryl-met-potenstel-sw443987.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/e98dbc34a136d2baa77465e2b97ec660.jpg/go-by-van-marcke-stelli-inbouwbad-duo-190x90x48cm-230l-wit-acryl-met-potenstel-sw443987.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ef7e853abff59b753a37c6c2eae6c83f.jpg/go-by-van-marcke-stelli-inbouwbad-duo-190x90x48cm-230l-wit-acryl-met-potenstel-sw443987.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/ec8ccdb69bdee7394fa603bd3ea4dc94.jpg/go-by-van-marcke-stelli-inbouwbad-duo-190x90x48cm-230l-wit-acryl-met-potenstel-sw443987.jpg", "https://static.rorix.nl/document/product/overig/a6330beac2a180c81c0ef02b4c6272e8.png", "https://static.rorix.nl/image/product/overig/2000x2000/e98dbc34a136d2baa77465e2b97ec660.jpg/go-by-van-marcke-stelli-inbouwbad-duo-190x90x48cm-230l-wit-acryl-met-potenstel-sw443987.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke inbouwbad',
  'GO by Van Marcke',
  247.99,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77203588/go-by-van-marcke-baldo-inbouwbad-duo-170x75x45cm-175l-met-potenstel-wit-acryl',
  'https://static.rorix.nl/image/product/overig/2000x2000/8e40b541c414dc61722170c0188c81dc.jpg/go-by-van-marcke-baldo-inbouwbad-duo-170x75x45cm-175l-met-potenstel-wit-acryl-sw443989.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/8e40b541c414dc61722170c0188c81dc.jpg/go-by-van-marcke-baldo-inbouwbad-duo-170x75x45cm-175l-met-potenstel-wit-acryl-sw443989.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9da729c7304d04ff986882b18433a428.jpg/go-by-van-marcke-baldo-inbouwbad-duo-170x75x45cm-175l-met-potenstel-wit-acryl-sw443989.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/2bcc201f6493d9a02cf294c533880539.jpg/go-by-van-marcke-baldo-inbouwbad-duo-170x75x45cm-175l-met-potenstel-wit-acryl-sw443989.jpg", "https://static.rorix.nl/document/product/overig/5e26710679a7f048deedc93f28cbd6c8.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8e40b541c414dc61722170c0188c81dc.jpg/go-by-van-marcke-baldo-inbouwbad-duo-170x75x45cm-175l-met-potenstel-wit-acryl-sw443989.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke inbouwbad',
  'GO by Van Marcke',
  179.99,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77404322/go-by-van-marcke-baldino-inbouwbad-170x70cm-zonder-poten-acryl-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/9d5c60fd962bf0092a37e6fc79853100.jpg/go-by-van-marcke-baldino-inbouwbad-170x70cm-zonder-poten-acryl-glans-wit-sw637135.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/9d5c60fd962bf0092a37e6fc79853100.jpg/go-by-van-marcke-baldino-inbouwbad-170x70cm-zonder-poten-acryl-glans-wit-sw637135.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/165ee44da4d16b3dcf3062cf5d2b254d.jpg/go-by-van-marcke-baldino-inbouwbad-170x70cm-zonder-poten-acryl-glans-wit-sw637135.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/9bd0ca1c8d815fde048db32f352167cc.jpg/go-by-van-marcke-baldino-inbouwbad-170x70cm-zonder-poten-acryl-glans-wit-sw637135.jpg", "https://static.rorix.nl/document/product/overig/06aaf071d8fd047dbb12c383b62bc32e.png", "https://static.rorix.nl/image/product/overig/2000x2000/9d5c60fd962bf0092a37e6fc79853100.jpg/go-by-van-marcke-baldino-inbouwbad-170x70cm-zonder-poten-acryl-glans-wit-sw637135.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke inbouwbad',
  'GO by Van Marcke',
  209.0,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77203591/go-by-van-marcke-todi-inbouwbad-170x75x40cm-190l-met-potenstel-wit-acryl',
  'https://static.rorix.nl/image/product/overig/2000x2000/18eef05a39ca21a9710c275a755506c7.jpg/go-by-van-marcke-todi-inbouwbad-170x75x40cm-190l-met-potenstel-wit-acryl-sw443992.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/18eef05a39ca21a9710c275a755506c7.jpg/go-by-van-marcke-todi-inbouwbad-170x75x40cm-190l-met-potenstel-wit-acryl-sw443992.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/860374d16e58c3f2ac75a2b1dda3fce1.jpg/go-by-van-marcke-todi-inbouwbad-170x75x40cm-190l-met-potenstel-wit-acryl-sw443992.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/cb3713216bd26c78d09239974a43b77a.jpg/go-by-van-marcke-todi-inbouwbad-170x75x40cm-190l-met-potenstel-wit-acryl-sw443992.jpg", "https://static.rorix.nl/document/product/overig/3827cd3d7b34e237dc12a2f16af69adc.jpg", "https://static.rorix.nl/document/product/overig/310d26204bcff0018a212534c3b96cfb.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke inbouwbad',
  'GO by Van Marcke',
  195.0,
  'baden',
  'budget',
  'https://www.sawiday.be/nl-be/p/77203587/go-by-van-marcke-todi-inbouwbad-160x70x38cm-140l-met-potenstel-wit-acryl',
  'https://static.rorix.nl/image/product/overig/2000x2000/18eef05a39ca21a9710c275a755506c7.jpg/go-by-van-marcke-todi-inbouwbad-160x70x38cm-140l-met-potenstel-wit-acryl-sw443988.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/18eef05a39ca21a9710c275a755506c7.jpg/go-by-van-marcke-todi-inbouwbad-160x70x38cm-140l-met-potenstel-wit-acryl-sw443988.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/860374d16e58c3f2ac75a2b1dda3fce1.jpg/go-by-van-marcke-todi-inbouwbad-160x70x38cm-140l-met-potenstel-wit-acryl-sw443988.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/d2d776555706026fe21106fc277ea9db.jpg/go-by-van-marcke-todi-inbouwbad-160x70x38cm-140l-met-potenstel-wit-acryl-sw443988.jpg", "https://static.rorix.nl/document/product/overig/5219bad2e388ff80a4f395f077194c5f.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/18eef05a39ca21a9710c275a755506c7.jpg/go-by-van-marcke-todi-inbouwbad-160x70x38cm-140l-met-potenstel-wit-acryl-sw443988.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Xellanz Duobad',
  'Xellanz',
  419.99,
  'baden',
  'premium',
  'https://www.sawiday.be/nl-be/p/76636196/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/53bfd06ae8df8.jpg/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit-sw72154.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/53bfd06ae8df8.jpg/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit-sw72154.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5af53d3a957f3.jpg/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit-sw72154.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5af53d3ae0fc6.jpg/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit-sw72154.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/53bfd068dd810.jpg/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit-sw72154.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/53bfd06d1b610.jpg/xellanz-portus-rd-inbouw-duo-ligbad-190x90x49-cm-acryl-glans-wit-sw72154.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Bette Starlet Duobad',
  'Bette',
  913.99,
  'baden',
  'luxury',
  'https://www.sawiday.be/nl-be/p/75631495/bette-starlet-bad-plaatstaal-dikwandig-rechthoekig-180x80x42cm-zonder-poten-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/83ddd068b53d15db0cadc3dea7ac81c5.jpg/bette-starlet-bad-plaatstaal-rechthoekig-180x80x42cm-wit-0341251.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/83ddd068b53d15db0cadc3dea7ac81c5.jpg/bette-starlet-bad-plaatstaal-rechthoekig-180x80x42cm-wit-0341251.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/765345.jpg/bette-starlet-bad-plaatstaal-rechthoekig-180x80x42cm-wit-0341251.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001206831.jpeg/bette-starlet-bad-plaatstaal-rechthoekig-180x80x42cm-wit-0341251.jpeg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/9f1fb9b3bc924f2147a35d5062e2934f.jpg/bette-starlet-bad-plaatstaal-rechthoekig-180x80x42cm-wit-0341251.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001206831.jpg/bette-starlet-bad-plaatstaal-rechthoekig-180x80x42cm-wit-0341251.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Hansgrohe Vernis Blend Regendouche',
  'Hansgrohe',
  431.71,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/77416411/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/de43c9f3897a10080de8a6432eccb482.jpg/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart-sw647136.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/de43c9f3897a10080de8a6432eccb482.jpg/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart-sw647136.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/4762b9860e3f71f0d3638a026c0f27f0.jpg/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart-sw647136.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d20fa1370dab7080cfbd855d9ee59d77.jpg/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart-sw647136.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9d782fe3ba75c2c3f8ddbb7e60c0aeb6.jpg/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart-sw647136.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5488e40766c9c76bbcffe636faedc494.jpg/hansgrohe-vernis-blend-showerpipe-met-thermostaat-ecosmart-mat-zwart-sw647136.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Hansgrohe Crometta s Regendouche',
  'Hansgrohe',
  371.3,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/76680801/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/c926fc195f636e5ff3537c6844cac8af.jpg/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom-sw73210.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c926fc195f636e5ff3537c6844cac8af.jpg/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom-sw73210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/99e6d6e5841af8215580dbbc9760065c.jpg/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom-sw73210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a42f919dbff7ae1ddfa6b884ceb2945e.jpg/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom-sw73210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/aca05c8c3e45ad49ae9ee3dca70a87ee.jpg/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom-sw73210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/80eb0afba870cf5a0af5170636190c49.jpg/hansgrohe-crometta-s-240-1jet-showerpipe-met-thermostaat-chroom-sw73210.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Hansgrohe Croma select s Doucheset',
  'Hansgrohe',
  1041.0,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77212670/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/f2ca7b54390e3e6563949c2bd05b996a.jpg/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart-sw451590.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/f2ca7b54390e3e6563949c2bd05b996a.jpg/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart-sw451590.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001421504.jpg/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart-sw451590.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/cb8db0b1acd69185563c6100c632825d.jpg/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart-sw451590.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/49a2ad9308f0a1a44c94093cd06bbec9.jpg/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart-sw451590.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e6eda753ac92122983e7d545d8d36d88.jpg/hansgrohe-croma-select-select-regendoucheset-thermostaat-air-1jet-ecosmart-croma-280-hoofddouche-handdouche-3-standen-mat-zwart-sw451590.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Grohe Euphoria Regendouche',
  'Grohe',
  866.0,
  'nl-be',
  'luxury',
  'https://www.sawiday.be/nl-be/p/76681289/grohe-euphoria-xxl-310-douchesysteem-supersteel',
  'https://static.rorix.nl/image/product/overig/2000x2000/938ab68e091c78752895fbf0a92f3e65.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-supersteel-sw73269.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/938ab68e091c78752895fbf0a92f3e65.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-supersteel-sw73269.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8171f20e60b2148c09522bde78b47a37.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-supersteel-sw73269.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3920bf60c89592e98e912895e55a683b.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-supersteel-sw73269.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0f8e8cc4777fb4a0331e08dba0a4d928.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-supersteel-sw73269.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001157068.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-supersteel-sw73269.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Grohe Euphoria Regendouche',
  'Grohe',
  863.0,
  'nl-be',
  'luxury',
  'https://www.sawiday.be/nl-be/p/76894770/grohe-euphoria-xxl-douchesysteem-met-douchekraan-thermostatisch-met-aquadimmer-met-rainshower-cosmo-310-hoofdd.-en-handd.-brushed-hard-graphite',
  'https://static.rorix.nl/image/product/overig/2000x2000/2c115a0a6c6c71ee15101f60df44c589.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-brushed-hard-graphite-sw98857.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/2c115a0a6c6c71ee15101f60df44c589.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-brushed-hard-graphite-sw98857.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7ba2e4b8257856d12b6a3054f0d7dd59.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-brushed-hard-graphite-sw98857.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/34598d557eaed3331df5223a490f9ad4.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-brushed-hard-graphite-sw98857.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001274262.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-brushed-hard-graphite-sw98857.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6d9e9daa5046bdb21dddb26be392b0b4.jpg/grohe-euphoria-xxl-regendoucheset-opbouw-hoofddouche-31cm-handdouche-rond-brushed-hard-graphite-sw98857.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Grohe smartcontrol Regendouche',
  'Grohe',
  899.0,
  'nl-be',
  'luxury',
  'https://www.sawiday.be/nl-be/p/76906605/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/287e1753dc9dc255c95c6d277659c7db.jpg/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom-sw108048.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/287e1753dc9dc255c95c6d277659c7db.jpg/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom-sw108048.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c1fbfea6c3be8f372384cd13329f80dc.jpg/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom-sw108048.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8965cd48ae99b01b74d2c5bb21bd534a.jpg/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom-sw108048.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6a2b9e565c078e3132fab57df01b03ff.jpg/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom-sw108048.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/592c73f82831e10f15893ea57e1fc83c.jpg/grohe-grohterm-smartcontrol-regendoucheset-inbouw-inbouwboxen-hoofddouche-vierkant-staafhanddouche-chroom-sw108048.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Slide Badwand',
  'Marenza',
  260.99,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/77254646/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/33e73bfddbe394f2da6f7aeaca5319c4.jpg/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart-sw491647.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/33e73bfddbe394f2da6f7aeaca5319c4.jpg/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart-sw491647.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a4a748fc711d7a5af6d64dc8e0355540.jpg/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart-sw491647.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ff7aa26b7929ecb58846bd3342ca6b56.jpg/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart-sw491647.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3a52cce7d073606f25959196098a6a1a.jpg/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart-sw491647.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/33e73bfddbe394f2da6f7aeaca5319c4.jpg/marenza-slide-quick-fit-badwand-2-delige-schuifdeur-170x150cm-6mm-veiligheidsglas-anti-kalk-mat-zwart-sw491647.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Slide Douchedeur',
  'Marenza',
  247.99,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/77254642/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/3ce2e342dc4550d69ace6c19f6a10611.jpg/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart-sw491643.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/3ce2e342dc4550d69ace6c19f6a10611.jpg/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart-sw491643.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f69d75f19a2091498128efc1dfcd8fe8.jpg/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart-sw491643.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/15033cf2d485f7edb47dacf3f39c204b.jpg/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart-sw491643.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c7664b5717c6e5506926c156390ac46c.jpg/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart-sw491643.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/26e20e93e4b9fbd601829672b7b701a0.jpg/marenza-slide-quick-fit-schuifdeur-100x190cm-6mm-veiligheidsglas-alu-profiel-anti-kalk-mat-zwart-sw491643.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Bellini Inloopdouche',
  'Marenza',
  309.99,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/77113686/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/d5e103af82e459bb70d9042c8629f9e3.jpg/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart-sw358009.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/d5e103af82e459bb70d9042c8629f9e3.jpg/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart-sw358009.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b5f356704cd3498ed9f9bae9be695a51.jpg/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart-sw358009.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e4dc542686ee53aee9f7a547bd50b6ee.jpg/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart-sw358009.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/eef46167db306b469ea0a289c96277f8.jpg/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart-sw358009.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/45ea950f01f2cd0c1a0ba1c1314be45a.jpg/marenza-bellini-inloopdouche-140x200cm-helder-glas-mat-zwart-sw358009.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Outdoor Buitendouche',
  'Fortifura',
  819.99,
  'nl-be',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77061896/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs',
  'https://static.rorix.nl/image/product/overig/2000x2000/d4611db1ebed6008cdc0e736d88c320d.jpg/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs--sw278130.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/d4611db1ebed6008cdc0e736d88c320d.jpg/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs--sw278130.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/72eebf4f23402efb990fd80cb679dcfa.jpg/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs--sw278130.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/09ae9f3d9e66a3fd6a7697bf4d377432.jpg/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs--sw278130.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2ba03daf042b9a8d3b476fd7372bbed3.jpg/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs--sw278130.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ee3a329258a3f68aa4ceed1a77f14745.jpg/fortifura-outdoor-deluxe-vrijstaande-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-regendouche-geborsteld-rvs-pvd-rvs--sw278130.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Outdoor Buitendouche',
  'Fortifura',
  719.99,
  'nl-be',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77061890/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs',
  'https://static.rorix.nl/image/product/overig/2000x2000/06890f4d2a790374f954364f97b3fc0e.jpg/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs--sw278124.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/06890f4d2a790374f954364f97b3fc0e.jpg/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs--sw278124.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/72eebf4f23402efb990fd80cb679dcfa.jpg/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs--sw278124.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/dbd5af47a01db4cfb30a056a17245d0a.jpg/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs--sw278124.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e599e8213fb25926418efeacc1783b1a.jpg/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs--sw278124.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2ba03daf042b9a8d3b476fd7372bbed3.jpg/fortifura-outdoor-original-buitendouche-geborsteld-rvs-pvd-rvs-316-handdouche-wandmodel-geborsteld-rvs-pvd-rvs--sw278124.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Galeria Inloopdouche',
  'Fortifura',
  527.99,
  'douche',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77691451/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/612571b542db77e7255b5c3f6cf221a5.jpg/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom-sw917216.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/612571b542db77e7255b5c3f6cf221a5.jpg/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom-sw917216.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d1e698b7353ff2f3f17d1dabdb05c5a9.jpg/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom-sw917216.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b8d16a67dbf78d5c1342556cd085673a.jpg/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom-sw917216.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a4859756262c32fee56cd2c6eb22e9d1.jpg/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom-sw917216.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/cc883d7a7bb3e8f7fb6ac20bc0f5899e.jpg/fortifura-galeria-inloopdouche-160x200cm-helder-glas-wandarm-chroom-sw917216.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Galeria Inloopdouche',
  'Fortifura',
  551.99,
  'douche',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77650786/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud',
  'https://static.rorix.nl/image/product/overig/2000x2000/38ea621f9a98b88265d22dde48d46a9d.jpg/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud--sw876748.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/38ea621f9a98b88265d22dde48d46a9d.jpg/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud--sw876748.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8967e2e61130e9498ee79cae95691ef6.jpg/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud--sw876748.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/76a356502d7696a18864685f46adac4d.jpg/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud--sw876748.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9c098d7a2bff450b559d04f62fcb14b4.jpg/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud--sw876748.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2721c728a9ba8036c8a0522db2cf1ab1.jpg/fortifura-galeria-inloopdouche-180x200cm-helder-glas-wandarm-geborsteld-messing-pvd-goud--sw876748.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Galeria Inloopdouche',
  'Fortifura',
  507.99,
  'douche',
  'premium',
  'https://www.sawiday.be/nl-be/p/77691476/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/bc11584dd7ce1491907ef457f00284a0.jpg/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart-sw917234.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/bc11584dd7ce1491907ef457f00284a0.jpg/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart-sw917234.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0b9e285d956086a83cc84bce73340233.jpg/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart-sw917234.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/29df8e19f7daca33211d75883e858c3e.jpg/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart-sw917234.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/35f52476376faa630f7b3a6cdd76309d.jpg/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart-sw917234.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/25ab0b70622f032bd21bc53a05e2cd8f.jpg/fortifura-galeria-inloopdouche-140x200cm-helder-glas-wandarm-mat-zwart-sw917234.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Galeria Inloopdouche',
  'Fortifura',
  556.99,
  'douche',
  'budget',
  'https://www.sawiday.be/nl-be/p/77733618/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd',
  'https://static.rorix.nl/image/product/overig/2000x2000/77ba4237c45bf441dd8bbe3e2c1b8646.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd-sw957389.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/77ba4237c45bf441dd8bbe3e2c1b8646.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd-sw957389.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/cc549799c607bba9ee8dec839e11b1b0.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd-sw957389.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d040186739ed47db94634d0635414004.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd-sw957389.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/77ba4237c45bf441dd8bbe3e2c1b8646.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd-sw957389.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/cc549799c607bba9ee8dec839e11b1b0.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-plafondarm-geborsteld-gunmetal-pvd-sw957389.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Galeria Inloopdouche',
  'Fortifura',
  491.99,
  'douche',
  'premium',
  'https://www.sawiday.be/nl-be/p/77650806/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd',
  'https://static.rorix.nl/image/product/overig/2000x2000/74f09bc5f08830fbc4e3b9c9389b3422.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd-sw876762.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/74f09bc5f08830fbc4e3b9c9389b3422.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd-sw876762.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e7c0d160a8dcb464cce4708f38ae6c04.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd-sw876762.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b5d842857fda1708fa31c95490587b83.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd-sw876762.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/add5e30bb77aab26a707fedc903a9b58.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd-sw876762.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8452d9e49eb41e943319ab25303fbe58.jpg/fortifura-galeria-inloopdouche-120x200cm-helder-glas-wandarm-geborsteld-gunmetal-pvd-sw876762.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Dawn Inloopdouche',
  'Adema',
  149.99,
  'douche',
  'budget',
  'https://www.sawiday.be/nl-be/p/78219386/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat',
  'https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443558.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443558.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/851de29541d034e22c98b0146021c872.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443558.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/35d46da267736595e3327363827f858a.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443558.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f44d5b523a02d56c654b15ccf5a96c9c.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443558.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443558.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Dawn Inloopdouche',
  'Adema',
  144.99,
  'douche',
  'budget',
  'https://www.sawiday.be/nl-be/p/78219381/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat',
  'https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443555.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443555.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/851de29541d034e22c98b0146021c872.jpg/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443555.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/35d46da267736595e3327363827f858a.jpg/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443555.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f44d5b523a02d56c654b15ccf5a96c9c.jpg/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443555.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-70x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1443555.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Dawn Inloopdouche',
  'Adema',
  159.99,
  'douche',
  'economy',
  'https://www.sawiday.be/nl-be/p/78228014/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat',
  'https://static.rorix.nl/image/product/overig/2000x2000/bf083041d1d57df4f80e58cc7965449c.jpg/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1451091.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/bf083041d1d57df4f80e58cc7965449c.jpg/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1451091.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a7f94fa317c1b1285d9d146d13a611b0.jpg/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1451091.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f27651d26a6fbe8237a28bcd818f99b3.jpg/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1451091.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/818d9f838cbd0147639613ba02ef1157.jpg/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1451091.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/bf083041d1d57df4f80e58cc7965449c.jpg/adema-dawn-inloopdouche-100x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1451091.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Dawn Inloopdouche',
  'Adema',
  149.99,
  'douche',
  'budget',
  'https://www.sawiday.be/nl-be/p/78219387/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat',
  'https://static.rorix.nl/image/product/overig/2000x2000/bf083041d1d57df4f80e58cc7965449c.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1443559.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/bf083041d1d57df4f80e58cc7965449c.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1443559.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a7f94fa317c1b1285d9d146d13a611b0.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1443559.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f27651d26a6fbe8237a28bcd818f99b3.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1443559.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/818d9f838cbd0147639613ba02ef1157.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1443559.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/bf083041d1d57df4f80e58cc7965449c.jpg/adema-dawn-inloopdouche-80x200cm-wandprofiel-stabilisatiestang-helder-glas-goud-mat-sw1443559.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Dawn Inloopdouche',
  'Adema',
  169.99,
  'douche',
  'economy',
  'https://www.sawiday.be/nl-be/p/78228018/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat',
  'https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1451095.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1451095.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/851de29541d034e22c98b0146021c872.jpg/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1451095.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/35d46da267736595e3327363827f858a.jpg/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1451095.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f44d5b523a02d56c654b15ccf5a96c9c.jpg/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1451095.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f2be440f51dbf86e2d493d7640e04687.jpg/adema-dawn-inloopdouche-120x200cm-wandprofiel-stabilisatiestang-helder-glas-zwart-mat-sw1451095.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Neptune Badwand',
  'Marenza',
  132.99,
  'douche',
  'budget',
  'https://www.sawiday.be/nl-be/p/77052597/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/e11fc6b0553eb8c5e1a7ddfe15a4f196.jpg/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom-sw238237.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/e11fc6b0553eb8c5e1a7ddfe15a4f196.jpg/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom-sw238237.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3ec02ea100eef856d6fe5640af40c0d5.jpg/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom-sw238237.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e64caa7fab2b79d377e382909225e7fb.jpg/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom-sw238237.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e11fc6b0553eb8c5e1a7ddfe15a4f196.jpg/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom-sw238237.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3ec02ea100eef856d6fe5640af40c0d5.jpg/marenza-neptune-badwand-1-delig-draaibaar-80x150cm-6mm-veiligheidsglas-anti-kalk-chroom-sw238237.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Bellini Inloopdouche',
  'Marenza',
  279.99,
  'douche',
  'economy',
  'https://www.sawiday.be/nl-be/p/77254661/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/d5e103af82e459bb70d9042c8629f9e3.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart-sw491662.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/d5e103af82e459bb70d9042c8629f9e3.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart-sw491662.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b5f356704cd3498ed9f9bae9be695a51.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart-sw491662.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e4dc542686ee53aee9f7a547bd50b6ee.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart-sw491662.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/eef46167db306b469ea0a289c96277f8.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart-sw491662.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/45ea950f01f2cd0c1a0ba1c1314be45a.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-mat-zwart-sw491662.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Bellini Inloopdouche',
  'Marenza',
  249.99,
  'douche',
  'economy',
  'https://www.sawiday.be/nl-be/p/75616752/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/c28956d08b597cc8188c2027fbfa6210.jpg/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom-sw2328.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c28956d08b597cc8188c2027fbfa6210.jpg/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom-sw2328.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e1766207e2cc601d08b5ee8c46b322aa.jpg/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom-sw2328.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5c18cac652365.jpg/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom-sw2328.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5c18cab8e1f6c.jpg/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom-sw2328.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5c18ca24ba055.jpg/marenza-bellini-inloopdouche-80x200cm-helder-glas-chroom-sw2328.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Marenza Bellini Inloopdouche',
  'Marenza',
  279.99,
  'douche',
  'economy',
  'https://www.sawiday.be/nl-be/p/77130318/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/80db8bd0d9e394f12e4c59952e80da42.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom-sw373908.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/80db8bd0d9e394f12e4c59952e80da42.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom-sw373908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e1766207e2cc601d08b5ee8c46b322aa.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom-sw373908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5c18cac652365.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom-sw373908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5c18cab8e1f6c.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom-sw373908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5c18ca24ba055.jpg/marenza-bellini-inloopdouche-110x200cm-helder-glas-chroom-sw373908.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Calvi Regendouche',
  'Fortifura',
  649.99,
  'kranen',
  'luxury',
  'https://www.sawiday.be/nl-be/p/78185762/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/b30728e1a9071e0a493d78e0519a67e1.jpg/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart-sw1412046.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/b30728e1a9071e0a493d78e0519a67e1.jpg/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart-sw1412046.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/4702644ef8abfdb1fddb71f22a1b25de.jpg/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart-sw1412046.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f508f91ba3075960eb4d8fadcfa1b300.jpg/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart-sw1412046.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ded93d2fc502fbfbb92f1ea0c50eb96c.jpg/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart-sw1412046.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3a1e6281f424181375e3f0fba8195ee3.jpg/fortifura-calvi-inbouw-regendoucheset-thermostatisch-wandarm-30cm-hoofddouche-staaf-handdouche-gladde-doucheslang-mat-zwart-sw1412046.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Calvi Regendouche',
  'Fortifura',
  499.99,
  'kranen',
  'premium',
  'https://www.sawiday.be/nl-be/p/77969588/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd',
  'https://static.rorix.nl/image/product/overig/2000x2000/1438049202a510ca5d7cabb98cb0cc4c.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd-sw1204408.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/1438049202a510ca5d7cabb98cb0cc4c.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd-sw1204408.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d296cf15618ad205ea60cbe37b9eb346.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd-sw1204408.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/06a229f55e3faa274fc7d9ac5253f194.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd-sw1204408.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8302dabaf3b533094c5b745561014b37.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd-sw1204408.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/45d6ac4ec2aaf346b6aa5397e1aeece7.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-metalen-slang-staaf-handdouche-geborsteld-gunmetal-pvd-sw1204408.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Calvi Regendouche',
  'Fortifura',
  499.99,
  'kranen',
  'premium',
  'https://www.sawiday.be/nl-be/p/77969586/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd',
  'https://static.rorix.nl/image/product/overig/2000x2000/8daf1cfe51592c824172c59da4b2a6be.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd-sw1204406.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/8daf1cfe51592c824172c59da4b2a6be.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd-sw1204406.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/42a290b071b3694161a9c3d8afb2930d.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd-sw1204406.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3fa4c1370ffb76a66027f532bd885f32.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd-sw1204406.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e529274b4a4ab83196ec91d923f45dde.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd-sw1204406.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8daf1cfe51592c824172c59da4b2a6be.jpg/fortifura-calvi-regendoucheset-thermostatisch-25cm-hoofddouche-gladde-slang-ronde-handdouche-geborsteld-gunmetal-pvd-sw1204406.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Calvi Douchekraan',
  'Fortifura',
  239.99,
  'kranen',
  'economy',
  'https://www.sawiday.be/nl-be/p/77495646/fortifura-calvi-thermostatische-inbouwkraan-2-wegs-inbouwdeel-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/a587dd9606a5a2ec6ce1a24f9b9a2b94.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-mat-zwart-sw721167.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/a587dd9606a5a2ec6ce1a24f9b9a2b94.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-mat-zwart-sw721167.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/df4ecd22b4e29e5e0219d13f4bea2d21.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-mat-zwart-sw721167.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/fbfff22e366c0533a44a4da23de9bbd6.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-mat-zwart-sw721167.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a587dd9606a5a2ec6ce1a24f9b9a2b94.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-mat-zwart-sw721167.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/df4ecd22b4e29e5e0219d13f4bea2d21.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-mat-zwart-sw721167.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Fortifura Calvi Douchekraan',
  'Fortifura',
  239.99,
  'kranen',
  'economy',
  'https://www.sawiday.be/nl-be/p/77495644/fortifura-calvi-thermostatische-inbouwkraan-2-wegs-inbouwdeel-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/d43767da8ebda6089b391bb4d0983aa5.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-chroom-sw721166.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/d43767da8ebda6089b391bb4d0983aa5.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-chroom-sw721166.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/cae49f37fa0c046400d672a9630e595d.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-chroom-sw721166.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/fbfff22e366c0533a44a4da23de9bbd6.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-chroom-sw721166.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3dde9e923ef407e571649576ef75da8b.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-chroom-sw721166.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d43767da8ebda6089b391bb4d0983aa5.jpg/fortifura-calvi-thermostatische-inbouwkraan-met-inbouwdeel-chroom-sw721166.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Sparkle 2.0 Regendouche',
  'Adema',
  149.99,
  'kranen',
  'budget',
  'https://www.sawiday.be/nl-be/p/77549622/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/40fcba7527bf8beff20425716bfc15d3.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom-sw773195.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/40fcba7527bf8beff20425716bfc15d3.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom-sw773195.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0c06061441053eca6bb280715531c337.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom-sw773195.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d48fb4693eb3cb5071d9fa58a9b7e525.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom-sw773195.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9a33ca23b5ab1aa4b5f806d1b14ab187.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom-sw773195.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b04a9d58b75593b06abe1aeb8ce83ddf.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-chroom-sw773195.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Sparkle 2.0 Regendouche',
  'Adema',
  149.99,
  'kranen',
  'budget',
  'https://www.sawiday.be/nl-be/p/77549625/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/bc3a99a7d99d2f83a79ce428cce20604.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart-sw773198.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/bc3a99a7d99d2f83a79ce428cce20604.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart-sw773198.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a1e7cb11ea678f57bc8f0da4fc6e91e4.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart-sw773198.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b70ad832922d0bbbbfdcccd7732f1527.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart-sw773198.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8a173ddee89921547d93e4e630451305.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart-sw773198.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/70c108b73bead1eedd46c46735e0ea53.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-20cm-handdouche-3-standen-zwart-sw773198.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Sparkle 2.0 Douchekraan',
  'Adema',
  74.99,
  'kranen',
  'budget',
  'https://www.sawiday.be/nl-be/p/77468198/adema-sparkle-20-thermostatische-douchekraan-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/c925fca05efd5a899935384f455d763b.jpg/adema-sparkle-2.0-thermostatische-douchekraan-chroom-sw696248.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c925fca05efd5a899935384f455d763b.jpg/adema-sparkle-2.0-thermostatische-douchekraan-chroom-sw696248.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6a357830246d924b18c302ff6eb74aec.jpg/adema-sparkle-2.0-thermostatische-douchekraan-chroom-sw696248.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c925fca05efd5a899935384f455d763b.jpg/adema-sparkle-2.0-thermostatische-douchekraan-chroom-sw696248.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6a357830246d924b18c302ff6eb74aec.jpg/adema-sparkle-2.0-thermostatische-douchekraan-chroom-sw696248.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c925fca05efd5a899935384f455d763b.jpg/adema-sparkle-2.0-thermostatische-douchekraan-chroom-sw696248.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Sparkle 2.0 Regendouche',
  'Adema',
  159.99,
  'kranen',
  'economy',
  'https://www.sawiday.be/nl-be/p/77549626/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/9d5a87ee9cc07c7431fa04d5dab1299a.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart-sw773199.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/9d5a87ee9cc07c7431fa04d5dab1299a.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart-sw773199.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5365dcc648f1ee087bb762e831c7539e.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart-sw773199.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b70ad832922d0bbbbfdcccd7732f1527.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart-sw773199.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8a173ddee89921547d93e4e630451305.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart-sw773199.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/70c108b73bead1eedd46c46735e0ea53.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-zwart-sw773199.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Sparkle 2.0 Regendouche',
  'Adema',
  159.99,
  'kranen',
  'economy',
  'https://www.sawiday.be/nl-be/p/77549624/adema-sparkle-20-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/ec7999531f1ff263d35f6223b2286827.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom-sw773197.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/ec7999531f1ff263d35f6223b2286827.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom-sw773197.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5e11d903a58354d0d9503d85c7eb2b50.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom-sw773197.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/01ca231c46e5a66d65fe0c24f6a5e754.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom-sw773197.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f17aab01eccb8d918348b4093c0138cb.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom-sw773197.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/336ccfcbeba5632fd4ab29d0bf0927a5.jpg/adema-sparkle-2.0-regendoucheset-thermostaat-hoofddouche-30cm-handdouche-3-standen-chroom-sw773197.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Exclusive Line Spiegel',
  'Adema',
  152.99,
  'Adema',
  'economy',
  'https://www.sawiday.be/nl-be/p/77018880/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/5be5972c5b26f.jpg/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart-sw209335.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/5be5972c5b26f.jpg/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart-sw209335.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b923fded080c.jpg/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart-sw209335.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b92359f2adfc.jpg/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart-sw209335.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b92359f8e1ab.jpg/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart-sw209335.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b92359fb88f9.jpg/adema-exclusive-line-spiegel-rond-100cm-frame-mat-zwart-sw209335.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Lonato Spiegel met verlichting',
  'Adema',
  216.99,
  'Adema',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77411541/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/a5fa86e1fefb1c4cc0537c9eb95ed147.jpg/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart-sw643231.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/a5fa86e1fefb1c4cc0537c9eb95ed147.jpg/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart-sw643231.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0aa07d0b12b98d07cc8aec0b0218aafc.jpg/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart-sw643231.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a96cef0781d4e2bc2137f7c6da903427.jpg/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart-sw643231.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ccd0e4df2588baabaaa5f88cda2388e6.jpg/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart-sw643231.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0d2daafa27e23dd0bc671c142fa0a960.jpg/adema-lonato-badkamerspiegel-rond-diameter-80cm-geintegreerde-led-verlichting-spiegelverwarming-infraroodbediening-mat-zwart-sw643231.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Lonato Spiegel met verlichting',
  'Adema',
  161.99,
  'Adema',
  'premium',
  'https://www.sawiday.be/nl-be/p/77411959/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud',
  'https://static.rorix.nl/image/product/overig/2000x2000/380189e383f61c049b232dc35df3f9bb.jpg/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud-sw643413.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/380189e383f61c049b232dc35df3f9bb.jpg/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud-sw643413.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/084ed517df84c175094376f56ae52869.jpg/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud-sw643413.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/62124120ae3646a8afb88ec7b9e05779.jpg/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud-sw643413.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/daf08e216b9de88a35ccb2ad5a6566fb.jpg/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud-sw643413.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2801978ae821e79b15603dee3929c0f9.jpg/adema-lonato-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-mat-goud-sw643413.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Exclusive Line Spiegel',
  'Adema',
  116.99,
  'Adema',
  'budget',
  'https://www.sawiday.be/nl-be/p/77018879/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/5be5972c5b26f.jpg/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart-sw209334.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/5be5972c5b26f.jpg/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart-sw209334.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b923fded080c.jpg/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart-sw209334.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b92359f2adfc.jpg/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart-sw209334.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b92359f8e1ab.jpg/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart-sw209334.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b92359fb88f9.jpg/adema-exclusive-line-spiegel-rond-80cm-frame-mat-zwart-sw209334.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Adema Exclusive Line Spiegel',
  'Adema',
  66.99,
  'Adema',
  'budget',
  'https://www.sawiday.be/nl-be/p/77256029/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/b863883e7053677e0efd2e4235cbee67.jpg/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit-sw492799.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/b863883e7053677e0efd2e4235cbee67.jpg/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit-sw492799.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/afccb85aecf01b6782d8fdd8a33289a7.jpg/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit-sw492799.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/dd8638bbafa6c8136635190658ee5812.jpg/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit-sw492799.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ba6af49e00f13042044001f7e7f563a1.jpg/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit-sw492799.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3866cf2cefb24904a3de1701b67e14ab.jpg/adema-exclusive-line-spiegel-rond-40cm-frame-mat-wit-sw492799.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Saniclass Spiegelverwarming',
  'Saniclass',
  69.99,
  'Saniclass',
  'budget',
  'https://www.sawiday.be/nl-be/p/710519/saniclass-spiegelverwarming-50x50cm',
  'https://static.rorix.nl/image/product/overig/2000x2000/d3140a08edac61880b346af0b286eff2.jpg/saniclass-spiegelverwarming-50x50cm-sw2185.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/d3140a08edac61880b346af0b286eff2.jpg/saniclass-spiegelverwarming-50x50cm-sw2185.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d3140a08edac61880b346af0b286eff2.jpg/saniclass-spiegelverwarming-50x50cm-sw2185.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d3140a08edac61880b346af0b286eff2.jpg/saniclass-spiegelverwarming-50x50cm-sw2185.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Saniclass Circle Spiegel met verlichting',
  'Saniclass',
  169.99,
  'Saniclass',
  'premium',
  'https://www.sawiday.be/nl-be/p/76907250/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar',
  'https://static.rorix.nl/image/product/overig/2000x2000/c24718f0763e444130d1dad8ecf0c192.jpg/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-sw108325.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c24718f0763e444130d1dad8ecf0c192.jpg/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-sw108325.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/371819a6227cb5dfdc603fe6eafe6aab.jpg/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-sw108325.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c169b27e2a1376d798929934133423e8.jpg/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-sw108325.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/581e457ab839ba9f4a581a2689f1790d.jpg/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-sw108325.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c016a6f31025d82c299a755817a222dc.jpg/saniclass-circle-badkamerspiegel-rond-diameter-60cm-indirecte-led-verlichting-spiegelverwarming-infrarood-schakelaar-sw108325.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Saniclass Prime Spiegelkast',
  'Saniclass',
  412.99,
  'Saniclass',
  'luxury',
  'https://www.sawiday.be/nl-be/p/77587323/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken',
  'https://static.rorix.nl/image/product/overig/2000x2000/199c43bc619d6d3e2c7019f9656ad38e.jpg/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken-sw815282.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/199c43bc619d6d3e2c7019f9656ad38e.jpg/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken-sw815282.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a78bb127ea1624b9df33122b9f47417e.jpg/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken-sw815282.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/199c43bc619d6d3e2c7019f9656ad38e.jpg/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken-sw815282.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a78bb127ea1624b9df33122b9f47417e.jpg/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken-sw815282.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/199c43bc619d6d3e2c7019f9656ad38e.jpg/saniclass-prime-spiegelkast-100x63x16cm-inclusief-zijpanelen-eiken-sw815282.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Saniclass Retro Line Spiegel',
  'Saniclass',
  104.99,
  'Saniclass',
  'economy',
  'https://www.sawiday.be/nl-be/p/77411975/saniclass-retro-line-2-0-spiegel-ovaal-90x38cm-frame-mat-zwart',
  'https://static.rorix.nl/image/product/overig/2000x2000/375499f9cf071f9b20d60aa158398027.jpg/saniclass-retro-line-2.0-spiegel-ovaal-90x38cm-frame-mat-zwart-sw643428.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/375499f9cf071f9b20d60aa158398027.jpg/saniclass-retro-line-2.0-spiegel-ovaal-90x38cm-frame-mat-zwart-sw643428.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6e0e719769235593afd9f0257c7d5861.jpg/saniclass-retro-line-2.0-spiegel-ovaal-90x38cm-frame-mat-zwart-sw643428.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e724f2fbb64e0f8659e38035dc17ed39.jpg/saniclass-retro-line-2.0-spiegel-ovaal-90x38cm-frame-mat-zwart-sw643428.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2e51094958d1391480cfe78996f3d9b1.jpg/saniclass-retro-line-2.0-spiegel-ovaal-90x38cm-frame-mat-zwart-sw643428.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/84a9e5158273b9d6e7d08907a75e9af4.jpg/saniclass-retro-line-2.0-spiegel-ovaal-90x38cm-frame-mat-zwart-sw643428.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Saniclass Chaci Spiegel',
  'Saniclass',
  89.99,
  'Saniclass',
  'budget',
  'https://www.sawiday.be/nl-be/p/77499606/saniclass-chaci-spiegel-80x70cm-4mm-incl-bevestingsmateriaal',
  'https://static.rorix.nl/image/product/overig/2000x2000/c66e160927596198957cf639883e07d4.jpg/saniclass-chaci-spiegel-80x70cm-4mm-incl.-bevestingsmateriaal-sw724611.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c66e160927596198957cf639883e07d4.jpg/saniclass-chaci-spiegel-80x70cm-4mm-incl.-bevestingsmateriaal-sw724611.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c66e160927596198957cf639883e07d4.jpg/saniclass-chaci-spiegel-80x70cm-4mm-incl.-bevestingsmateriaal-sw724611.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/c66e160927596198957cf639883e07d4.jpg/saniclass-chaci-spiegel-80x70cm-4mm-incl.-bevestingsmateriaal-sw724611.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Smedbo Outline Vergrootspiegel',
  'Smedbo',
  134.99,
  'Smedbo',
  'budget',
  'https://www.sawiday.be/nl-be/p/77307949/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom',
  'https://static.rorix.nl/image/product/overig/2000x2000/70cc2f645be42d222f6c50f76d3c2c24.jpg/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom-sw542096.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/70cc2f645be42d222f6c50f76d3c2c24.jpg/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom-sw542096.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/65853c39d2835985eb5d5e34e3f530be.jpg/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom-sw542096.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/70cc2f645be42d222f6c50f76d3c2c24.jpg/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom-sw542096.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/65853c39d2835985eb5d5e34e3f530be.jpg/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom-sw542096.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/70cc2f645be42d222f6c50f76d3c2c24.jpg/smedbo-cosmeticaspiegel-wand-20cm-7x-vergrotend-verlichting-messing-chroom-sw542096.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit D-code WC-bril',
  'Duravit',
  61.25,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/34825/duravit-d-code-closetzitting',
  'https://static.rorix.nl/image/product/overig/2000x2000/edf877d121b5d4bcc262a8e9b124f455.jpg/duravit-d-code-wc-zitting-43x36x4cm-compact-kunststof-wit-glanzend-0315127.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/edf877d121b5d4bcc262a8e9b124f455.jpg/duravit-d-code-wc-zitting-43x36x4cm-compact-kunststof-wit-glanzend-0315127.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7be703b2ebfa9538607e4ccc8902f86f.jpg/duravit-d-code-wc-zitting-43x36x4cm-compact-kunststof-wit-glanzend-0315127.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0a7b02ff045974ed871b5f05f39f2e0a.jpg/duravit-d-code-wc-zitting-43x36x4cm-compact-kunststof-wit-glanzend-0315127.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/eee29f98fe9fff875fb85717846fb614.jpg/duravit-d-code-wc-zitting-43x36x4cm-compact-kunststof-wit-glanzend-0315127.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f81296696971f7aa29f8e0d72e49f7ab.jpg/duravit-d-code-wc-zitting-43x36x4cm-compact-kunststof-wit-glanzend-0315127.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit Starck 3 WC-bril',
  'Duravit',
  118.32,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/6867/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/1a625f90cb36dd866cef65596dc69b46.jpg/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit-0290272.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/1a625f90cb36dd866cef65596dc69b46.jpg/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit-0290272.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f26c12c72a8dd6b55587eb9e0a5857b0.jpg/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit-0290272.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9e7ae2658935db3731453c4b2d36e6e7.jpg/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit-0290272.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/730f69bba6a75fdfc80e85f9351d13c7.jpg/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit-0290272.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/97f3b0fe1de2784937bba213e22f828a.jpg/duravit-starck-3-wc-zitting-37x43.1x4.3cm-softclose-quickrelease-kunststof-glans-wit-0290272.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit D-neo Hangtoilet',
  'Duravit',
  396.0,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/77311110/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans',
  'https://static.rorix.nl/image/product/overig/2000x2000/6b73b396b637c105be5b3a9167a14514.jpg/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans-sw544305.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/6b73b396b637c105be5b3a9167a14514.jpg/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans-sw544305.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6287a5b26c85f170b1c8272b676e825a.jpg/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans-sw544305.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e8721773ff763559b96b56ad490c9ae5.jpg/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans-sw544305.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/553ee90a55ba940f5bd9054b5416610f.jpg/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans-sw544305.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/4d5e9b63b1d856bdb6cbfd64be77b25b.jpg/duravit-d-neo-wandtoilet-met-zitting-37x54x40cm-wit-hoogglans-sw544305.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit Sensowash Douche WC',
  'Duravit',
  2810.0,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77179885/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/83775c520f9872eeef29cd3052f91c9e.jpg/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit-sw420600.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/83775c520f9872eeef29cd3052f91c9e.jpg/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit-sw420600.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/36e114ef0c800182189404c5c0813de3.jpg/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit-sw420600.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2694736b8190ebd3e92ee69e7f925089.jpg/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit-sw420600.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/470857e7fadc0aff8f9aab003a8e58fb.jpg/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit-sw420600.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7ae2c2e9be65c7d6f18a12fc896a6df3.jpg/duravit-sensowash-starck-f-lite-douchewc-37.8x57.5cm-spoelrandloos-met-closetzitting-glans-wit-sw420600.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch Subway 3.0 Hangtoilet',
  'Villeroy & Boch',
  439.0,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/77313318/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin',
  'https://static.rorix.nl/image/product/overig/2000x2000/a93f6213ba318a46d1d24f9e4a3b5654.jpg/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin-sw546736.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/a93f6213ba318a46d1d24f9e4a3b5654.jpg/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin-sw546736.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ec841357d5dd0b1b7dc86c5957bccf74.jpg/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin-sw546736.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/505d5d1ac748674b3492672ce73e2b2f.jpg/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin-sw546736.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7403033288fed86f99784690a47109ff.jpg/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin-sw546736.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f29bde51f3a21c68c46035af08a7a2fa.jpg/villeroy-boch-subway-3.0-wandcloset-pack-56cm-zonder-spoelrand-diepspoel-twistflush-softclose-en-quickrelease-zitting-ceramic-wit-alpin-sw546736.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch Subway 2.0 Hangtoilet',
  'Villeroy & Boch',
  486.99,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/76108417/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/7eb63557fbcb9b8cb885b468daee4770.jpg/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit-ga59210.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/7eb63557fbcb9b8cb885b468daee4770.jpg/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit-ga59210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ac85512a1a5d236c72c49286e07bf540.jpg/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit-ga59210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e5cfbb730fb2638246dd36aec861aa56.jpg/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit-ga59210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/73bf1962b504679d7ce303e7378549d1.jpg/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit-ga59210.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8efbdf6d7329306cce33a872f945ca9f.jpg/villeroy-boch-subway-2.0-wandcloset-directflush-slimseat-zitting-softclose-quick-release-ceramicplus-glans-wit-ga59210.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch O.novo Duoblok toilet',
  'Villeroy & Boch',
  418.04,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/76834869/villeroy-boch-o.novo-combipack-duobloccomb.met-qr-plus-sc-zitting-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/b7c4a99464922c268f45e76de126a97c.jpg/villeroy-boch-o.novo-combipack-duobloccombinatie-met-quickrelease-en-softclose-zitting-ceramic-wit-alphin-sw85730.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/b7c4a99464922c268f45e76de126a97c.jpg/villeroy-boch-o.novo-combipack-duobloccombinatie-met-quickrelease-en-softclose-zitting-ceramic-wit-alphin-sw85730.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001263830.jpeg/villeroy-boch-o.novo-combipack-duobloccombinatie-met-quickrelease-en-softclose-zitting-ceramic-wit-alphin-sw85730.jpeg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001263829.jpeg/villeroy-boch-o.novo-combipack-duobloccombinatie-met-quickrelease-en-softclose-zitting-ceramic-wit-alphin-sw85730.jpeg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001263829.jpg/villeroy-boch-o.novo-combipack-duobloccombinatie-met-quickrelease-en-softclose-zitting-ceramic-wit-alphin-sw85730.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001263830.jpg/villeroy-boch-o.novo-combipack-duobloccombinatie-met-quickrelease-en-softclose-zitting-ceramic-wit-alphin-sw85730.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch O.novo Hangtoilet',
  'Villeroy & Boch',
  211.38,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/76568262/villeroy-en-boch-o.novo-combi-pack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/2616660ca60cc1b5fe8096be0e2fdfc1.jpg/villeroy-boch-o.novo-combipack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit-sw68876.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/2616660ca60cc1b5fe8096be0e2fdfc1.jpg/villeroy-boch-o.novo-combipack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit-sw68876.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f2605c3660e4527745b39db829ec96d7.jpg/villeroy-boch-o.novo-combipack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit-sw68876.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/22e553b619dad906915d077f3f43a754.jpg/villeroy-boch-o.novo-combipack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit-sw68876.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e959dde9b621b5754117bd91f3870048.jpg/villeroy-boch-o.novo-combipack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit-sw68876.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/e8a6112e8fa56f4ebacea75c8770e074.jpg/villeroy-boch-o.novo-combipack-met-compact-wandcloset-diepspoel-directflush-36x49cm-met-zitting-met-softclose-en-quick-release-wit-sw68876.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Ideal Standard Tesi Hangtoilet',
  'Ideal Standard',
  250.99,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/76618752/ideal-standard-tesi-pack-wandwc-in-verglaasd-porselein.-aquablade.-535x365-mm.-wit-wc-zitting-softclose.-wit',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/040100-high.jpg/ideal-standard-tesi-wand-wc-keramiek-aquablade-53,5x36,5cm-wit-met-wc-zitting-softclose-wit-sw71259.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/040100-high.jpg/ideal-standard-tesi-wand-wc-keramiek-aquablade-53,5x36,5cm-wit-met-wc-zitting-softclose-wit-sw71259.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5877414885f5d.jpeg/ideal-standard-tesi-wand-wc-keramiek-aquablade-53,5x36,5cm-wit-met-wc-zitting-softclose-wit-sw71259.jpeg", "https://static.rorix.nl/image/product/overig/2000x2000/5877414fb7c67.jpeg/ideal-standard-tesi-wand-wc-keramiek-aquablade-53,5x36,5cm-wit-met-wc-zitting-softclose-wit-sw71259.jpeg", "https://static.rorix.nl/image/product/overig/2000x2000/58774156eb2dc.jpeg/ideal-standard-tesi-wand-wc-keramiek-aquablade-53,5x36,5cm-wit-met-wc-zitting-softclose-wit-sw71259.jpeg", "https://static.rorix.nl/image/product/overig/2000x2000/587741658706a.jpeg/ideal-standard-tesi-wand-wc-keramiek-aquablade-53,5x36,5cm-wit-met-wc-zitting-softclose-wit-sw71259.jpeg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Geberit QeramiQ Dely Toiletset',
  'Geberit',
  456.99,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/77426930/qeramiq-dely-toiletset-geberit-up100-inbouwreservoir-witte-bedieningsplaat-toilet-zitting-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/989716211d8adcb1430437d2be34d28f.jpg/qeramiq-dely-toiletset-geberit-up100-inbouwreservoir-witte-bedieningsplaat-toilet-zitting-glans-wit-sw656671.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/989716211d8adcb1430437d2be34d28f.jpg/qeramiq-dely-toiletset-geberit-up100-inbouwreservoir-witte-bedieningsplaat-toilet-zitting-glans-wit-sw656671.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6093b146a82f19a44ff26d9b9e94c43b.jpg/qeramiq-dely-toiletset-geberit-up100-inbouwreservoir-witte-bedieningsplaat-toilet-zitting-glans-wit-sw656671.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ad31a61186501bc8d0d99fa14b354b8a.jpg/qeramiq-dely-toiletset-geberit-up100-inbouwreservoir-witte-bedieningsplaat-toilet-zitting-glans-wit-sw656671.jpg", "https://static.rorix.nl/document/product/overig/c14afd2d21e623e2fdaf439d9404b6e1.jpg", "https://static.rorix.nl/document/product/overig/e7641a61408dcb3571b36af01c8e87ab.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Geberit Bedieningspaneel',
  'Geberit',
  50.12,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/75649460/geberit-sigma01-bedieningsplaat-2-toets-spoeling-rond-alpien-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/5723022a33af9.jpg/geberit-sigma01-bedieningsplaat-2-toets-spoeling-ronde-knoppen-alpien-wit-0700518.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/5723022a33af9.jpg/geberit-sigma01-bedieningsplaat-2-toets-spoeling-ronde-knoppen-alpien-wit-0700518.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/53eb8218676e2.jpg/geberit-sigma01-bedieningsplaat-2-toets-spoeling-ronde-knoppen-alpien-wit-0700518.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D1300012503744.jpg/geberit-sigma01-bedieningsplaat-2-toets-spoeling-ronde-knoppen-alpien-wit-0700518.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9156a2dab2bfcf4bb5c5850999c3019d.jpg/geberit-sigma01-bedieningsplaat-2-toets-spoeling-ronde-knoppen-alpien-wit-0700518.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/c64ba7fa32a5bd42ef4a41f3337a9daa.jpg/geberit-sigma01-bedieningsplaat-2-toets-spoeling-ronde-knoppen-alpien-wit-0700518.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Geberit AquaClean Douche WC',
  'Geberit',
  3328.0,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/76880183/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/fd8beef5790e0b8f80c33fb642032ab9.jpg/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit-sw87549.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/fd8beef5790e0b8f80c33fb642032ab9.jpg/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit-sw87549.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5d1b09122240cdba4c8f417981920721.jpg/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit-sw87549.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/456ffac3267873e7b135061c3e2a075e.jpg/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit-sw87549.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/612c85809e2002f08d71cb8ca4c1950e.jpg/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit-sw87549.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a9db7f61cce4d17f527698436814dd3a.jpg/geberit-aquaclean-mera-classic-douche-wc-geurafzuiging-warme-luchtdroging-ladydouche-softclose-glans-wit-sw87549.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke Tina Duoblok toilet',
  'GO by Van Marcke',
  220.14,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/77072895/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit',
  'https://static.rorix.nl/image/product/van-marcke/2000x2000/319f14832f1a02b6ee6fad93bad3ce37.jpg/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit-sw288421.jpg',
  '["https://static.rorix.nl/image/product/van-marcke/2000x2000/319f14832f1a02b6ee6fad93bad3ce37.jpg/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit-sw288421.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/66058be000eecd041e87b724b95f3022.jpg/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit-sw288421.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/7dd86cafa8a86b083d762299265a781b.jpg/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit-sw288421.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9cad1e36b2e7199a0f668cc706f90a61.jpg/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit-sw288421.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/0ed3a7541e40c6bd802228aec06121ab.jpg/go-by-van-marcke-tina-pack-staand-toilet-zonder-spoelrand-met-reservoir-met-geberit-spoelmechanisme-met-dunne-softclose-en-takeoff-zitting-wit-sw288421.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Differnz Helios Fonteinset',
  'Differnz',
  114.99,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77020174/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/5b69a00eafbc5.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit-sw209752.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/5b69a00eafbc5.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit-sw209752.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b69a00f56175.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit-sw209752.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b69a00f75f90.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit-sw209752.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b69a00f00f25.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit-sw209752.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b69a00f24ee6.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-links-recht-chromen-kraan-keramiek-wit-sw209752.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Differnz Jukon Fonteinset',
  'Differnz',
  144.99,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77011995/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs',
  'https://static.rorix.nl/image/product/overig/2000x2000/5af5770f7df64.jpg/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs-sw205843.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/5af5770f7df64.jpg/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs-sw205843.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b1791678e99b.jpg/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs-sw205843.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5af5770fb6860.jpg/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs-sw205843.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5af5770fd616b.jpg/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs-sw205843.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b169eb1e9ec2.jpg/differnz-jukon-fonteinset-38.5x18.5x9cm-rechthoek-1-kraangat-rechts-zwart-beton-grijs-sw205843.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Differnz Helios Fonteinset',
  'Differnz',
  127.99,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/76087372/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/b8c59bb76894e830bfa21690e7ffde45.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit-sw21908.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/b8c59bb76894e830bfa21690e7ffde45.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit-sw21908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/d0c2e3da34d50f9f16949f49644eea3f.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit-sw21908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2596135e70ec789a167fc2f2f37e8a31.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit-sw21908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5b69a00f75f90.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit-sw21908.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8557a3447c8614c5c8bd9cb07ff730b0.jpg/differnz-helios-fonteinset-37.5x18.5x9.5cm-rechthoek-1-kraangat-rechts-recht-chromen-kraan-keramiek-wit-sw21908.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Differnz Ravo Fonteinset',
  'Differnz',
  227.99,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/77129693/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/04ae180c044a92c4cec2c726058d8cd2.jpg/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit-sw373162.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/04ae180c044a92c4cec2c726058d8cd2.jpg/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit-sw373162.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2c330d77a4069b3705ffffec2e3554fa.jpg/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit-sw373162.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/b9a5eee4971f0f9452d9b0765c0d7873.jpg/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit-sw373162.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8bbdbeda86f37c18bf722f682698caac.jpg/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit-sw373162.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ca8290137925565ad702bbae94c97b07.jpg/differnz-ravo-fonteinset-38.5x18.5x25cm-rechthoek-1-kraangat-gebogen-matte-zwarte-kraan-met-zwart-frame-keramiek-wit-sw373162.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Differnz Hura Fonteinset',
  'Differnz',
  141.99,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77069896/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/7ceae8a8ec97aedfcfd75921daead60a.jpg/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit-sw285500.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/7ceae8a8ec97aedfcfd75921daead60a.jpg/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit-sw285500.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/15d9635452da16b3143ab4ccb2a62682.jpg/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit-sw285500.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a73088d4e44cdc13828620e06a3753bb.jpg/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit-sw285500.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/f493b10d6a5a6d26bad2a032b8632aed.jpg/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit-sw285500.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/5772ee001b62b0f40d2e48c864f3dd1f.jpg/differnz-hura-fonteinset-37.5x18.5x9cm-rechthoek-1-kraangat-zwart-mat-rechte-kraan-keramiek-wit-sw285500.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Geberit 300 basic Uitstortgootsteen',
  'Geberit',
  179.45,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77176503/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/7bcdd500dd102e9ed5417b09b765eb65.jpg/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit-sw417651.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/7bcdd500dd102e9ed5417b09b765eb65.jpg/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit-sw417651.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001406360.jpg/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit-sw417651.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8a3a183e3403944270edb9fb8777690d.jpg/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit-sw417651.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/21dd88dbde0d5d57ef22599e9dfaea71.jpg/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit-sw417651.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/570f551acf56ef1ed7ffef556b56e8f0.jpg/geberit-300-basic-norma-uitstortgootsteen-met-stootrand-35x45x35cm-met-gaten-voor-emmerrooster-wit-sw417651.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Ideavit Solidharmony Lavabo',
  'Ideavit',
  470.0,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/76892383/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/fe04cc6663d376886b7bbefebf1b9f8e.jpg/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit-sw97025.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/fe04cc6663d376886b7bbefebf1b9f8e.jpg/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit-sw97025.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/1a9fdd2b0b9637aa7656a5cd21051327.jpg/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit-sw97025.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/6f8333a8af48307d39b60f5ce009e25f.jpg/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit-sw97025.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/06111557c765aca1e227bd21fba49e6e.jpg/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit-sw97025.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/8d11f975ba1721407535d8a5c75fed86.jpg/ideavit-solidharmony-opbouwwastafel-40x13cm-solid-surface-mat-wit-sw97025.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Ideavit Solidthin Waskom',
  'Ideavit',
  340.0,
  'nl-be',
  'premium',
  'https://www.sawiday.be/nl-be/p/76835328/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/c9265b316f3a80ef3cdd871c2b658451.jpg/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit-sw85902.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/c9265b316f3a80ef3cdd871c2b658451.jpg/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit-sw85902.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/a4795f4f36a33a0941f26832182d6d43.jpg/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit-sw85902.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/32155b36982549eec99994ef9115c800.jpg/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit-sw85902.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/70a8b85c5bf0741ff31cb8c98c5dc9d5.jpg/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit-sw85902.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/245ddd210412c24392b9c8ac0dcd870b.jpg/ideavit-solidthin-opbouw-wastafel-39x39x14.5cm-rond-0-kraangaten-1-wasbak-solid-surface-wit-sw85902.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Villeroy & Boch O.novo Uitstortgootsteen',
  'Villeroy & Boch',
  215.0,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/53079/villeroy-en-boch-o-novo-uitstortgootsteen-45x35cm-met-stootrand-wit-69120101',
  'https://static.rorix.nl/image/product/overig/2000x2000/2e4c08ce2d7caeb3054da18324f15fe3.jpg/villeroy-boch-o.novo-omnia-pro-uitstortgootsteen-met-stootrand-zonder-emmerrooster-wit-0140415.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/2e4c08ce2d7caeb3054da18324f15fe3.jpg/villeroy-boch-o.novo-omnia-pro-uitstortgootsteen-met-stootrand-zonder-emmerrooster-wit-0140415.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/ad809715f7562c0349d3fbd7bd932e64.jpg/villeroy-boch-o.novo-omnia-pro-uitstortgootsteen-met-stootrand-zonder-emmerrooster-wit-0140415.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/12a2161b3f1d4bb64c962f90d0bbf636.jpg/villeroy-boch-o.novo-omnia-pro-uitstortgootsteen-met-stootrand-zonder-emmerrooster-wit-0140415.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/3a08459c23a593c2659a41819df877e1.jpg/villeroy-boch-o.novo-omnia-pro-uitstortgootsteen-met-stootrand-zonder-emmerrooster-wit-0140415.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001263884.jpg/villeroy-boch-o.novo-omnia-pro-uitstortgootsteen-met-stootrand-zonder-emmerrooster-wit-0140415.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'GO by Van Marcke Spoelbak',
  'GO by Van Marcke',
  170.99,
  'nl-be',
  'budget',
  'https://www.sawiday.be/nl-be/p/77067898/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-onderkast-80-cm',
  'https://static.rorix.nl/image/product/overig/2000x2000/9ba3f8bedb6f16c465629a45868ed9ce.jpg/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-sw283656.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/9ba3f8bedb6f16c465629a45868ed9ce.jpg/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-sw283656.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/8750090bacd3a082f7d512b03df980b4.jpg/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-sw283656.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9ba3f8bedb6f16c465629a45868ed9ce.jpg/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-sw283656.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/8750090bacd3a082f7d512b03df980b4.jpg/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-sw283656.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/9ba3f8bedb6f16c465629a45868ed9ce.jpg/go-by-van-marcke-molto-inbouwspoeltafel-composiet-met-2-bakken-met-afdruip-1170-x-500-mm-met-vierkante-manuele-plug-omkeerbaar-zwart-sw283656.jpg"]'::jsonb,
  NOW()
);
INSERT INTO products (name, brand, price, category, price_tier, url, primary_image_url, images, created_at) VALUES (
  'Duravit Starck 3 Uitstortgootsteen',
  'Duravit',
  231.87,
  'nl-be',
  'economy',
  'https://www.sawiday.be/nl-be/p/53075/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit',
  'https://static.rorix.nl/image/product/overig/2000x2000/2a9c36b35af875e0f52fc620f3a5f104.jpg/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit-0291271.jpg',
  '["https://static.rorix.nl/image/product/overig/2000x2000/2a9c36b35af875e0f52fc620f3a5f104.jpg/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit-0291271.jpg", "https://static.rorix.nl/image/product/galvano/2000x2000/D130001001311545.jpg/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit-0291271.jpg", "https://static.rorix.nl/image/product/van-marcke/2000x2000/5533535d9c4d548d259da7edfdf90c18.jpg/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit-0291271.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/04043a47a00baa8cf597ae181109659d.jpg/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit-0291271.jpg", "https://static.rorix.nl/image/product/overig/2000x2000/2a9c36b35af875e0f52fc620f3a5f104.jpg/duravit-starck-3-uitstortgootsteen-48x42,5-cm-wit-0291271.jpg"]'::jsonb,
  NOW()
);

COMMIT;
