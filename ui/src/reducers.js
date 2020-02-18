import { combineReducers } from 'redux';

import usersReducer from './pages/Users/reducers';
import publishersReducer from './pages/Publishers/reducers';
import contentReducer from './pages/Content/reducers';

export default combineReducers({
  usersReducer,
  publishersReducer,
  contentReducer,
});
