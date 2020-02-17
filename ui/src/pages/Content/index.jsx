import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core';

import Table from '../../components/ResponsiveTable';

import {
  fetchContent as fetchContentAction,
  setFilters as setFiltersAction,
  addContent as addContentAction,
  updateContent as updateContentAction,
  deleteContent as deleteContentAction,
} from './actions.js';

import { contentPreview } from './helpers.js';
import Form from './components/Form';

const styles = theme => ({
  controls: {
    marginBottom: theme.spacing(2),
  },
});


class Content extends React.Component {
  state = {
    form: {
      open: false,
      data: null,
    },
  };

  columns = [
    {
      key: 'name',
      title: 'Имя',
    },
    {
      key: 'preview',
      title: 'Предпросмотр',
      getValue: item => contentPreview(item.src),
    },
    {
      key: 'comment',
      title: 'Комментарий',
    },
    {
      key: 'created_at',
      title: 'Дата создания',
    }
  ];
  actions = [
    {
      key: 'edit',
      title: 'Редактировать',
      onClick: item => this.showForm(item),
      color: 'primary',
    },
    {
      key: 'delete',
      title: 'Удалить',
      onClick: item => this.deleteContent(item),
      color: 'secondary',
    },
  ];

  componentDidMount() {
    const { fetchContent } = this.props;
    fetchContent();
  }

  handleFiltersChange = (filters) => {
    const { setFilters, fetchContent } = this.props;
    setFilters(filters);
    fetchContent();
  };

  setPage = (page) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, page })
  };

  setLimit = (limit) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, limit, page: 1 })
  };

  showForm = (data=null) => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: true, data }
    }))
  };

  hideForm = () => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: false, data: null }
    }))
  };

  handleFormSubmit = (formData) => {
    const { form: { data } } = this.state;
    const { fetchContent, addContent, updateContent } = this.props;
    const newFromData = new FormData();
    newFromData.set('comment', formData.comment);
    newFromData.append('file', formData.file);
    if (data && data.id) {
      updateContent(newFromData, data.id, () => {
        fetchContent();
        this.hideForm();
      })
    } else {
      addContent(newFromData, () => {
        fetchContent();
        this.hideForm();
      })
    }
  };

  deleteContent = (content) => {
    const { fetchContent, deleteContent } = this.props;
    // TODO: make confirm dialog
    if (confirm(`Удалить контент ${content.name}`)) {
      deleteContent(content.id, () => {
        fetchContent()
      })
    }
  };

  render() {
    const { form } = this.state;
    const { classes, content, filters, total } = this.props;
    return (
      <>
        {form.open &&
          <Form
            data={form.data}
            handleClose={this.hideForm}
            handleSubmit={this.handleFormSubmit} />
        }
        <div className={classes.controls}>
          <Button
            variant='contained'
            color='primary'
            onClick={this.showForm}>
            Добавить контент
          </Button>
        </div>
        <Table
          items={content}
          columns={this.columns}
          actions={this.actions}
          page={filters.page}
          onPageChange={this.setPage}
          limit={filters.limit}
          onLimitChange={this.setLimit}
          total={total} />
      </>
    );
  }
}

Content.propTypes = {
  content: PropTypes.array.isRequired,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchContent: PropTypes.func.isRequired,
  setFilters: PropTypes.func.isRequired,
  addContent: PropTypes.func.isRequired,
  updateContent: PropTypes.func.isRequired,
  deleteContent: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = ({ contentReducer }) => ({ ...contentReducer });

const mapDispatchToProps = {
  fetchContent: fetchContentAction,
  setFilters: setFiltersAction,
  addContent: addContentAction,
  updateContent: updateContentAction,
  deleteContent: deleteContentAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(styles)(Content));
