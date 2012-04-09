Ext.define('Screener.store.Sites', {
    extend: 'Ext.data.Store',
    //requires: 'Screener.model.Site',
    model: 'Screener.model.Site',
    autoLoad: true,
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
            read    : 'site',
            create  : 'site?action=create',
            update  : 'site?action=update',
            destroy : 'site?action=update'
        },
        reader: {
            type: 'json',
            root: 'results',
            successProperty: 'success'
        }
    }
});