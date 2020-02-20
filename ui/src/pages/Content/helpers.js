import React from 'react'

// TODO: upgrade it for many content formats
export function contentPreview(src) {
  if (src.includes('.mp4' || '.mov' || '.avi')) {
    return (<video controls height={150} src={`/${src}`}/>)
  }
  if (src.includes('.png' || '.jpg' || '.gif')) {
    return (<img height={150} alt='some' src={`/${src}`}/>)
  }
  return (<div>Неподдерживаемый формат</div>)
}