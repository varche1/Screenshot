Ext.define('Screener.view.site.Edit', {
    extend: 'Ext.window.Window',
    alias: 'widget.siteedit',
    
    title       : 'Edit Site',
    layout      : 'fit',
    autoShow    : true,
    modal       : true,
    
    initComponent: function() {
        
        this.items = [{
            xtype: 'form',
            border: false,
            bodyPadding: 10,
            fieldDefaults: {
                labelStyle: 'font-weight:bold'
            },
            defaults: {
                margins: '0 0 10 0'
            },
            items: [{
                xtype: 'textfield',
                name : 'title',
                fieldLabel: 'Title',
                width: 400,
                value: 'webpp.ru'
            },{
                xtype: 'textfield',
                name : 'url',
                fieldLabel: 'URL',
                width: 400,
                value: 'http://www.webpp.ru'
            }]
        }];

        this.buttons = [{
            text: 'Save',
            action: 'save'
        },{
            text: 'Cancel',
            scope: this,
            handler: this.close
        }];
        
        this.callParent();
    }
});