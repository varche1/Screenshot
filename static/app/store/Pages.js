Ext.define('Screener.store.Pages', {
    extend: 'Ext.data.Store',
    //requires: 'Screener.model.Site',
    model: 'Screener.model.Page',
    //autoLoad: true,
    autoSync: true,
    
    proxy: {
        type: 'ajax',
        //batchActions: false,
        actionMethods: {
            read    : 'GET',
            create  : 'PUT',
            update  : 'POST',
            destroy : 'DELETE',
        },
        api: {
            read    : 'page',
            create  : 'page?action=create',
            update  : 'page?action=update',
            destroy : 'page?action=update'
        },
        reader: {
            type: 'json',
            root: 'results',
            successProperty: 'success'
        }
    }
});