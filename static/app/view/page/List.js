Ext.define('Screener.view.page.List', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.pagelist',
    
    store: 'Pages',
    
    title: 'Pages',
    hideHeaders: false,
    
    initComponent: function() {
        
        this.selModel = Ext.create('Ext.selection.CheckboxModel');
        
        this.columnLines = true;
        
        this.columns = [
            { text: 'Title', dataIndex: 'title'},
            { text: 'URL', dataIndex: 'url', flex: 1 },
            { text: 'Screens' },
        ];
        
        this.dockedItems = [{
            xtype: 'toolbar',
            items: [{
                xtype: 'button',
                text:'Add',
                iconCls: 'page-add',
                action: 'add',
                disabled: true
            },{
                xtype: 'button',
                text: 'Edit',
                iconCls: 'page-edit',
                action: 'edit',
                disabled: true
            },{
                xtype: 'button',
                text: 'Delete',
                iconCls: 'page-delete',
                action: 'delete',
                disabled: true
            },{
                xtype: 'button',
                text: 'Filter shots',
                iconCls: 'shots-filter',
                action: 'shots-filter',
                disabled: true
            },{
                xtype: 'button',
                text: 'Make shots',
                iconCls: 'shots-make',
                action: 'shots-make',
                disabled: true
            }]
        }];
        
        this.callParent();
    }
});