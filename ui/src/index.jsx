import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';

import rootReducer from './reducers';
import runSagas from './sagas';
import Root from './components/Root';
import Users from './pages/Users';
import Publishers from './pages/Publishers';
import Content from './pages/Content';
import Devices from './pages/Devices';

const sagaMiddleware = createSagaMiddleware();
const store = createStore(rootReducer, applyMiddleware(sagaMiddleware));

runSagas(sagaMiddleware);
render(
  <Provider store={store}>
    <BrowserRouter basename="/admin/">
      <Root>
        <Switch>
          <Route path="/users/" component={Users} exact />
          <Route path="/publishers/" component={Publishers} exact />
          <Route path="/content/" component={Content} exact />
          <Route path="/devices/" component={Devices} exact />
        </Switch>
      </Root>
    </BrowserRouter>
  </Provider>,
  document.getElementById('app'),
);
