Ext.define('Screener.controller.Sites', {
    extend: 'Ext.app.Controller',
    
    views: [
        'site.List',
        'site.Edit'
    ],
    
    refs: [{
        ref: 'siteList',
        selector: 'sitelist'
    }],
    
    stores: ['Sites', 'Pages'],
    models: ['Site'],
    
    init: function() {
        this.control({
            'sitelist': {
                selectionchange: this.onSiteSelect
            },
            'sitelist button[action=add]': {
                click: this.addSite
            },
            'sitelist button[action=edit]': {
                click: this.editSite
            },
            'sitelist button[action=delete]': {
                click: this.deleteSite
            },
            'siteedit button[action=save]': {
                click: this.updateSite
            }
        });
    },
    
    onSiteSelect: function(grid, record) {
        if (!record.length) return;
        
        this.getSiteList().down('button[action=edit]').setDisabled(false);
        this.getSiteList().down('button[action=delete]').setDisabled(false);
        this.application.fireEvent('pagesload', record[0]);
    },
    
    addSite: function(button) {
        Ext.widget('siteedit').down('form');
    },
    
    editSite: function(button) {
        var selection = this.getSiteList().selModel.getSelection();
        if (!selection.length){
            Ext.MessageBox.alert('Status', 'Please, select a Site'); return;
        }
        Ext.widget('siteedit').down('form').loadRecord(selection[0]);
    },
    
    updateSite: function(button) {
        var win    = button.up('window'),
            form   = win.down('form'),
            record = form.getRecord(),
            values = form.getValues(),
            store  = this.getSitesStore();
        
        if (!record)
            store.add(values);
        else
            record.set(values);
        
        win.close();
    },
    
    deleteSite: function(button, noAsk) {
        var self = this;
        if (noAsk !== true) {
            Ext.MessageBox.confirm('Confirm', 'Delete the Site?', function(button){ self.deleteSite(button, noAsk=true) }); return;
        }
        
        if (button == 'no')
            return;
        
        var selection = this.getSiteList().selModel.getSelection();
        if (!selection.length) {
            Ext.MessageBox.alert('Status', 'Please, select a Site'); return;
        }
        
        this.getSitesStore().remove(selection[0]);
    }
});
