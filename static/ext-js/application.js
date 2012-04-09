Ext.require(['*']);

Ext.onReady(function() {
    
    var addSiteWin;

    function addSiteWinHadler() {
        if (!addSiteWin) {
            addSiteWin = Ext.widget('window', {
                title: 'Add Site',
                closeAction: 'hide',
                width: 400,
                height: 150,
                layout: 'fit',
                resizable: false,
                //modal: true,
                items: Ext.widget('form', {
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    border: false,
                    bodyPadding: 10,
                    fieldDefaults: {
                        labelAlign: 'top',
                        labelWidth: 100,
                        labelStyle: 'font-weight:bold'
                    },
                    defaults: {
                        margins: '0 0 10 0'
                    },
                    items: [{
                        xtype: 'textfield',
                        fieldLabel: 'Site URL',
                        vtype: 'url',
                        name: 'site',
                        allowBlank: false
                    }],
                    buttons: [
                        {
                            text: 'Cancel',
                            handler: function() {
                                this.up('form').getForm().reset();
                                this.up('window').hide();
                            }
                        }, {
                            text: 'Save',
                            handler: function() {
                                if (this.up('form').getForm().isValid()) {
                                    // In a real application, this would submit the form to the configured url
                                    // this.up('form').getForm().submit();
                                    this.up('form').getForm().reset();
                                    this.up('window').hide();
                                    Ext.MessageBox.alert('Thank you!', 'Your inquiry has been sent. We will respond as soon as possible.');
                                }
                            }
                        }
                    ]
                })
            });
        }
        addSiteWin.show();
    }
    
    Ext.create('Ext.Viewport', {
        layout: {
            type: 'border',
            padding: 5
        },
        title: 'Ext Layout Browser',
        defaults: {
            split: true
        },
        items: [
        {
            xtype: 'box',
            id: 'header',
            region: 'north',
            html: '<h1> Ext.Layout.Browser</h1>',
            height: 15
        },{
            region: 'west',
            //collapsible: true,
            //title: 'Starts at width 30%',
            split: false,
            width: 200,
            minHeight: 140,
            html: 'west<br>I am floatable',
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'top',
                items: [
                    {
                        xtype: 'button',
                        itemId: 'toggleCw',
                        text: 'Добавить Сайт',
                        handler: addSiteWinHadler
                    }
                ]
            }]
        },{
            region: 'center',
            collapsible: true,
            title: 'Starts at width 30%',
            split: false,
            width: 200,
            //minWidth: 100,
            minHeight: 140,
            html: 'west<br>I am floatable'
        }]
    });
});
