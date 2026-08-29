export const IMAGE_LIMIT_BYTES = 10 * 1024 * 1024;
export const IMAGE_TYPES = ['image/jpeg','image/png','image/webp'];

export function validateImage(file) {
  if (!file) throw new Error('Please select an image.');
  if (!IMAGE_TYPES.includes(file.type)) throw new Error('Use JPG, PNG, or WebP.');
  if (file.size > IMAGE_LIMIT_BYTES) throw new Error('Image must be 10 MB or smaller.');
  return true;
}

export function previewImage(file, imgElement) {
  validateImage(file);
  const url = URL.createObjectURL(file);
  imgElement.src = url;
  imgElement.onload = () => URL.revokeObjectURL(url);
  return url;
}

export async function submitImageVideo({endpoint, file, prompt, negativePrompt='', duration=4, fps=16}) {
  validateImage(file);
  if (!prompt?.trim()) throw new Error('Motion prompt is required.');
  const body = new FormData();
  body.append('image', file, file.name);
  body.append('prompt', prompt.trim());
  body.append('negative_prompt', negativePrompt);
  body.append('duration', String(duration));
  body.append('fps', String(fps));
  const response = await fetch(`${endpoint.replace(/\/$/,'')}/api/generate/image-to-video`, {method:'POST', body});
  const data = await response.json().catch(()=>({}));
  if (!response.ok) throw new Error(data.detail || 'Image-to-video request failed.');
  return data;
}
