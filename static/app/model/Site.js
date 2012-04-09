Ext.define('Screener.model.Site', {
    extend: 'Ext.data.Model',
    idProperty: '_id',
    fields: [
        {name: '_id', useNull: true},
        'title',
        'url'
    ],
});