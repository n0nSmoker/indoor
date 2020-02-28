import rootSagas from 'components/Root/sagas';
import usersSagas from 'pages/Users/sagas';
import publishersSagas from 'pages/Publishers/sagas';
import contentSagas from 'pages/Content/sagas';
import devicesSagas from 'pages/Devices/sagas';


export default function runSagas(sagaMiddleware) {
  sagaMiddleware.run(rootSagas);
  sagaMiddleware.run(usersSagas);
  sagaMiddleware.run(publishersSagas);
  sagaMiddleware.run(contentSagas);
  sagaMiddleware.run(devicesSagas);
}
