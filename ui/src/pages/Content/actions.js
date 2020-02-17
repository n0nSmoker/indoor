import {
  CONTENT_ACTION_FETCH_CONTENT,
  CONTENT_ACTION_SET_FILTERS,
  CONTENT_ACTION_ADD_CONTENT,
  CONTENT_ACTION_UPDATE_CONTENT,
  CONTENT_ACTION_DELETE_CONTENT,
} from './consts.js';


export const fetchContent = () => ({ type: CONTENT_ACTION_FETCH_CONTENT });
export const setFilters = filters => ({ type: CONTENT_ACTION_SET_FILTERS, filters });
export const addContent = (formData, callback) => ({ type: CONTENT_ACTION_ADD_CONTENT, formData, callback });
export const updateContent = (formData, contentId, callback) => ({ type: CONTENT_ACTION_UPDATE_CONTENT, formData, contentId, callback });
export const deleteContent = (contentId, callback) => ({ type: CONTENT_ACTION_DELETE_CONTENT, contentId, callback });
