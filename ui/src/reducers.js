import { combineReducers } from 'redux';

import headerReducer from './components/Header/reducers';
import usersReducer from './pages/Users/reducers';
import publishersReducer from './pages/Publishers/reducers';
import contentReducer from './pages/Content/reducers';

export default combineReducers({
  headerReducer,
  usersReducer,
  publishersReducer,
  contentReducer,
});
