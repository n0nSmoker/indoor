import usersSagas from './pages/Users/sagas';
import publishersSagas from './pages/Publishers/sagas';
import contentSagas from './pages/Content/sagas';

export default function runSagas(sagaMiddleware) {
  sagaMiddleware.run(usersSagas);
  sagaMiddleware.run(publishersSagas);
  sagaMiddleware.run(contentSagas);
}
