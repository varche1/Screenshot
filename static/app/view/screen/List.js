Ext.define('Screener.view.screen.List', {
    extend: 'Ext.Panel',
    alias: 'widget.screenlist',
    
    autoScroll: true,
    bodyPadding: 5,
    initComponent: function() {
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