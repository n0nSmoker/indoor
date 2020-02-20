import {
  CONTENT_ACTION_FETCH_CONTENT,
  CONTENT_ACTION_SET_FILTERS,
  CONTENT_ACTION_MUTATE_CONTENT,
  CONTENT_ACTION_DELETE_CONTENT,
} from './consts.js';


export const fetchContent = () => ({ type: CONTENT_ACTION_FETCH_CONTENT });

export const mutateContent = (contentData, callback) => ({ type: CONTENT_ACTION_MUTATE_CONTENT, payload: contentData, callback });

export const deleteContent = (contentId, callback) => ({ type: CONTENT_ACTION_DELETE_CONTENT, contentId, callback });

export const setFilters = filters => ({ type: CONTENT_ACTION_SET_FILTERS, filters });
