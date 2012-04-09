Ext.define('Screener.model.Page', {
    extend: 'Ext.data.Model',
    idProperty: '_id',
    fields: [
        {name: '_id', useNull: true},
        'site',
        'title',
        'url'
    ],
});