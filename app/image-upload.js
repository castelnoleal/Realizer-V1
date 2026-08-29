const TYPES = new Set(['image/jpeg','image/png','image/webp']);
const MAX = 10 * 1024 * 1024;
export function validateImage(file){if(!file)throw new Error('Choose an image first.');if(!TYPES.has(file.type))throw new Error('Use JPG, PNG, or WebP.');if(file.size>MAX)throw new Error('Image must be 10 MB or smaller.');return file;}
export function bindImageUpload({input,dropZone,preview,onChange}){
  const accept=f=>{try{validateImage(f); preview.src=URL.createObjectURL(f); preview.hidden=false; dropZone.classList.add('has-image'); onChange?.(f);}catch(e){onChange?.(null,e);}};
  input.addEventListener('change',()=>accept(input.files?.[0]));
  ['dragenter','dragover'].forEach(x=>dropZone.addEventListener(x,e=>{e.preventDefault();dropZone.classList.add('dragging')}));
  ['dragleave','drop'].forEach(x=>dropZone.addEventListener(x,e=>{e.preventDefault();dropZone.classList.remove('dragging')}));
  dropZone.addEventListener('drop',e=>accept(e.dataTransfer.files?.[0]));
  return ()=>{preview.src='';preview.hidden=true;dropZone.classList.remove('has-image');input.value='';onChange?.(null)};
}
