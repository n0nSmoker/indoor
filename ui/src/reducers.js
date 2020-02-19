import { combineReducers } from 'redux';

import headerReducer from './components/Header/reducers';
import notificationReducer from './components/Notifications/reducers';
import usersReducer from './pages/Users/reducers';
import publishersReducer from './pages/Publishers/reducers';
import contentReducer from './pages/Content/reducers';

export default combineReducers({
  headerReducer,
  notificationReducer,
  usersReducer,
  publishersReducer,
  contentReducer,
});
