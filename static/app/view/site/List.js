Ext.define('Screener.view.site.List', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.sitelist',
    
    store: 'Sites',
    
    title: 'Sites',
    hideHeaders: true,
    
    initComponent: function() {
        this.columns = [{
            dataIndex: 'title',
            flex: 1
        },{
            dataIndex: 'url',
            flex: 1
        }];
        
        this.dockedItems = [{
            xtype: 'toolbar',
            items: [{
                xtype: 'button',
                text:'Add',
                iconCls: 'site-add',
                action: 'add'
            },{
                xtype: 'button',
                text: 'Edit',
                iconCls: 'site-edit',
                action: 'edit',
                disabled: true
            },{
                xtype: 'button',
                text: 'Delete',
                iconCls: 'site-delete',
                action: 'delete',
                disabled: true
            }]
        }];
        
        this.callParent();
    }
});