import usersSagas from './pages/Users/sagas';
import publishersSagas from './pages/Publishers/sagas';

export default function runSagas(sagaMiddleware) {
  sagaMiddleware.run(usersSagas);
  sagaMiddleware.run(publishersSagas);
}
