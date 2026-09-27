import { mkdir, writeFile } from 'node:fs/promises';
const photos = {
  clinical: 'photo-1576091160399-112ba8d25d1d',
  pricing: 'photo-1584308666744-24d5c474f2ae',
  claims: 'photo-1450101499163-c8848c66ca85',
  mortgage: 'photo-1560518883-ce09059eeffa'
};
await mkdir('site/assets', { recursive: true });
for (const [name, id] of Object.entries(photos)) {
  const response = await fetch(`https://images.unsplash.com/${id}?w=1400&q=85&fit=crop`);
  if (!response.ok) throw new Error(`${name}: ${response.status}`);
  await writeFile(`site/assets/${name}.jpg`, Buffer.from(await response.arrayBuffer()));
  console.log(`Downloaded ${name}`);
}
