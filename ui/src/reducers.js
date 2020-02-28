import { combineReducers } from 'redux';

import rootReducer from 'components/Root/reducers';
import headerReducer from 'components/Header/reducers';
import notificationReducer from 'components/Notifications/reducers';
import usersReducer from 'pages/Users/reducers';
import publishersReducer from 'pages/Publishers/reducers';
import contentReducer from 'pages/Content/reducers';
import devicesReducer from 'pages/Devices/reducers';

export default combineReducers({
  rootReducer,
  headerReducer,
  notificationReducer,
  usersReducer,
  publishersReducer,
  contentReducer,
  devicesReducer,
});
