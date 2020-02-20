import {
  PUBLISHERS_ACTION_FETCH_PUBLISHERS,
  PUBLISHERS_ACTION_SET_FILTERS,
  PUBLISHERS_ACTION_MUTATE_PUBLISHER,
  PUBLISHERS_ACTION_DELETE_PUBLISHER,
} from './consts.js';


export const fetchPublishers = () => ({ type: PUBLISHERS_ACTION_FETCH_PUBLISHERS });

export const mutatePublisher = (publisherData, callback) => ({
  type: PUBLISHERS_ACTION_MUTATE_PUBLISHER,
  payload: publisherData,
  callback
});

export const deletePublisher = publisherId => ({ type: PUBLISHERS_ACTION_DELETE_PUBLISHER, payload: publisherId });

export const setFilters = filters => ({ type: PUBLISHERS_ACTION_SET_FILTERS, filters });
