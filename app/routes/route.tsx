import { NextApiResponse } from 'next';
import nextConnect from 'next-connect';
import formidable from 'formidable';
import fs from 'fs';
import path from 'path';

export const config = {
  api: {
    bodyParser: false,
  },
};

const uploadDir = path.join(process.cwd(), 'public', 'uploaded_images');
console.log('Upload directory path:', uploadDir);

if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
  console.log('Upload directory created.');
} else {
  console.log('Upload directory already exists.');
}

const handler = nextConnect<NextApiRequest, NextApiResponse>();

handler.use(async (req, res, next) => {
  const form = new formidable.IncomingForm();
  form.uploadDir = uploadDir;
  form.keepExtensions = true;

  console.log('Formidable form configured.');

  form.parse(req, (err, fields, files) => {
    console.log('Form parsing started.');

    if (err) {
      console.error('Form parsing error:', err);
      return res.status(500).json({ error: 'Failed to upload file' });
    }

    console.log('Form parsing completed.');
    console.log('Fields:', fields);
    console.log('Files:', files);

    const file = files.file as formidable.File;
    const filePath = `/public/${path.basename(file.path)}`;
    console.log('File path:', filePath);

    req.body = { filePath, fields, files };
    next();
  });
});

handler.post((req, res) => {
  res.status(200).json(req.body);
});

export default handler;
