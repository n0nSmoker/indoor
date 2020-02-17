import { combineReducers } from 'redux';

import usersReducer from './pages/Users/reducers';
import publishersReducer from './pages/Publishers/reducers';

export default combineReducers({
  usersReducer,
  publishersReducer,
});
