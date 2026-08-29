// Browser-side contract shared by all future providers.
export const MODES = Object.freeze({
  TEXT_TO_VIDEO: 'text-to-video',
  IMAGE_TO_VIDEO: 'image-to-video',
  TEXT_IMAGE_TO_VIDEO: 'text-image-to-video'
});

export function validateGenerationInput(input) {
  if (!input?.prompt?.trim()) throw new Error('Prompt is required.');
  if (!Object.values(MODES).includes(input.mode)) throw new Error('Invalid generation mode.');
  if (input.mode !== MODES.TEXT_TO_VIDEO && !input.image) throw new Error('Upload an image first.');
  return true;
}
