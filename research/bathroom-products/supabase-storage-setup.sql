-- Create storage bucket for product images
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('product-images', 'product-images', true, 5242880, 
        ARRAY['image/jpeg', 'image/png', 'image/webp']);

-- Public read policy for catalog images (UI display)
CREATE POLICY "Public read product images"
ON storage.objects FOR SELECT
USING (bucket_id = 'product-images')
TO public
WITH CHECK (object IS NOT NULL);

-- Authenticated upload policy for render images (AI generation)
CREATE POLICY "Authenticated upload product images"
ON storage.objects FOR INSERT
WITH CHECK (auth.role() = 'authenticated');
