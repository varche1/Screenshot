Ext.define('Screener.controller.Pages', {
    extend: 'Ext.app.Controller',
    
    views: [
        'page.List',
        'page.Edit',
        'screen.Edit',
        'screen.List'
    ],
    
    refs: [{
        ref: 'pageList',
        selector: 'pagelist'
    },{
        ref: 'screenList',
        selector: 'screenlist'
    }],
    
    stores: ['Pages'],
    models: ['Page'],
    params: {},
    
    init: function() {
        this.control({
            'pagelist': {
                selectionchange: this.onPageSelect
            },
            'pagelist button[action=add]': {
                click: this.addPage
            },
            'pagelist button[action=edit]': {
                click: this.editPage
            },
            'pagelist button[action=delete]': {
                click: this.deletePage
            },
            'pagelist button[action=shots-filter]': {
                click: this.getShotsFilterForm
            },
            'pagelist button[action=shots-make]': {
                click: this.makeShots
            },
            'pageedit button[action=save]': {
                click: this.updatePage
            },
            'shotsfilter button[action=save]': {
                click: this.saveFilter
            }
        });
        
        this.application.on({
            pagesload: this.onPagesLoad,
            scope: this
        });
    },
    
    onPagesLoad: function(site) {
        this.getPageList().down('button[action=add]').setDisabled(false);
        this.getPageList().down('button[action=edit]').setDisabled(true);
        this.getPageList().down('button[action=delete]').setDisabled(true);
        this.getPageList().down('button[action=shots-filter]').setDisabled(false);
        this.getPageList().down('button[action=shots-make]').setDisabled(true);
        
        this.params = {};
        this.params.siteId = site.get('_id');
        this.getPagesStore().load({
            params: {
                site: site.get('_id')
            },
            scope: this
        });
    },
    
    onPageSelect: function(grid, record) {
        this.getPageList().down('button[action=edit]').setDisabled(false);
        this.getPageList().down('button[action=delete]').setDisabled(false);
        this.application.fireEvent('screenload', record[0]);
    },
    
    addPage: function(grid, record) {
        Ext.widget('pageedit').down('form');
    },
    
    editPage: function(grid, record) {
        var selection = this.getPageList().selModel.getSelection();
        if (!selection.length){
            Ext.MessageBox.alert('Status', 'Please, select a Page'); return;
        }
        Ext.widget('pageedit').down('form').loadRecord(selection[0]);
    },
    
    updatePage: function(button) {
        var win    = button.up('window'),
            form   = win.down('form'),
            record = form.getRecord(),
            values = form.getValues(),
            store  = this.getPagesStore();
        
        if (!record){
            values.site = this.params.siteId;
            store.add(values);
        }
        else
            record.set(values);
        
        win.close();
    },
    
    deletePage: function(button, noAsk) {
        var self = this;
        if (noAsk !== true) {
            Ext.MessageBox.confirm('Confirm', 'Delete the Page?', function(button){ self.deletePage(button, noAsk=true) }); return;
        }
        
        if (button == 'no')
            return;
        
        var selection = this.getPageList().selModel.getSelection();
        if (!selection.length) {
            Ext.MessageBox.alert('Status', 'Please, select a Page'); return;
        }
        
        this.getPagesStore().remove(selection[0]);
    },
    
    getShotsFilterForm: function(button) {
        Ext.widget('shotsfilter').down('form');
    },
    
    saveFilter: function(button) {
        var values = button.up('window').down('form').getValues();
        this.params.filer = values;
        log(values);
        this.getPageList().down('button[action=shots-make]').setDisabled(false);
    },
    
    makeShots: function(button) {
        var selection = this.getPageList().selModel.getSelection();
        if (!selection.length) {
            Ext.MessageBox.alert('Status', 'Please, select some Pages'); return;
        }
        
        var filter = this.params.filer;
        if (!filter) {
            Ext.MessageBox.alert('Status', 'Please, select choose Filter'); return;
        }
        
        filter.pages = Tools.getFieldFromModels(selection, '_id');
        
        Ext.Ajax.request({
            url: '/screen',
            params: Ext.encode(filter),
            success: function(response){
                console.log(Ext.decode(response.responseText));
            }
        });
    }
});
