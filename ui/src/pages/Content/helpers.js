import React from 'react'

// TODO: upgrade it for many content formats
export function contentPreview(src) {
  if (src.includes('.mp4') || src.includes('.mov')) {
    return (<video controls height={150} src={`/${src}`}/>)
  }
  return (<img height={150} alt='some' src={`/${src}`}/>)
}