import {
  PUBLISHERS_ACTION_FETCH_PUBLISHERS,
  PUBLISHERS_ACTION_SET_FILTERS,
  PUBLISHERS_ACTION_ADD_PUBLISHER,
  PUBLISHERS_ACTION_UPDATE_PUBLISHER,
  PUBLISHERS_ACTION_DELETE_PUBLISHER,
} from './consts.js';


export const fetchPublishers = () => ({ type: PUBLISHERS_ACTION_FETCH_PUBLISHERS });
export const setFilters = filters => ({ type: PUBLISHERS_ACTION_SET_FILTERS, filters });
export const addPublisher = (formData, callback) => ({ type: PUBLISHERS_ACTION_ADD_PUBLISHER, formData, callback });
export const updatePublisher = (formData, publisherId, callback) => ({ type: PUBLISHERS_ACTION_UPDATE_PUBLISHER, formData, publisherId, callback });
export const deletePublisher = (publisherId, callback) => ({ type: PUBLISHERS_ACTION_DELETE_PUBLISHER, publisherId, callback });
