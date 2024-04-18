odoo.define('pos_route_config.weight_scale_helper', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var widgetRegistry = require('web.widget_registry');
    var FieldManagerMixin = require('web.FieldManagerMixin');


    async function sleep(msec) {
        return new Promise(resolve => setTimeout(resolve, msec));
    }

    var StWeightScale = Widget.extend(FieldManagerMixin, {
        init: function (parent, model, context) {
            this._super(parent);
            FieldManagerMixin.init.call(this);
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            var html = '<button id="btn_st_weight_scale" class="btn btn-link"><i class="fa fa-balance-scale"/> Usar báscula</button>';
            this.$el.html(html);
            this.$('#btn_st_weight_scale').click(function (ev) {
                $("input[name='st_weight_aux']").select();
                $("input[name='st_weight_aux']").on('keyup', async (e) => {
                    if (e.which === 119) {
                        // $("input[name='st_weight_aux']").val('9.99');
                        await sleep(3000);
                        $("input[name='st_percent']").select();
                    }
                    else{
                        // console.log($("div[name='can_writing_weight'] input:first").is(':checked'))
                        if($("div[name='can_writing_weight'] input:first").is(':checked')) {
                            const element =  $("input[name='st_weight_aux']").val();
                            // console.log('valor inicial ' + element);
                            const newText = element.replace(/[^.\d]/g, '');
                            // const newText = element.replace(/\s/g, '').replace(/\D/g, '');
                            // const newText = element.replace(/./g, '0.00');
                            // console.log('nuevo valor ' + newText);
                            $("input[name='st_weight_aux']").val(newText);
                        }
                        else {
                            
                            if($("input[name='st_weight_aux']").val() === '0.00') {
                                $("input[name='st_weight_aux']").select();
                            }
                            else{
                                // console.log('valor inicial ' + $("input[name='st_weight_aux']").val());
                                // console.log('nuevo valor ' + '0.00');
                                $("input[name='st_weight_aux']").val('0.00');
                                $("input[name='st_weight_aux']").select();
                            }
                        }
                    }
                    
                });
            });
        },
    });

    var EnWeightScale = Widget.extend(FieldManagerMixin, {
        init: function (parent, model, context) {
            this._super(parent);
            FieldManagerMixin.init.call(this);
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            var html = '<button id="btn_en_weight_scale" class="btn btn-link"><i class="fa fa-balance-scale"/> Usar báscula</button>';
            this.$el.html(html);
            this.$('#btn_en_weight_scale').click(function (ev) {
                $("input[name='en_weight_aux']").select();
                $("input[name='en_weight_aux']").on('keyup', async (e) => {
                    if (e.which === 119) {
                        // $("input[name='en_weight_aux']").val('9.99');
                        await sleep(500);
                        $("input[name='en_percent']").select();
                    }
                    else{
                        // console.log($("div[name='can_writing_weight'] input:first").is(':checked'))
                        if($("div[name='can_writing_weight'] input:first").is(':checked')) {
                            const element =  $("input[name='en_weight_aux']").val();
                            // console.log('valor inicial ' + element);
                            const newText = element.replace(/[^.\d]/g, '');
                            // const newText = element.replace(/\s/g, '').replace(/\D/g, '');
                            // const newText = element.replace(/./g, '0.00');
                            // console.log('nuevo valor ' + newText);
                            $("input[name='en_weight_aux']").val(newText);
                        }
                        else {
                            
                            if($("input[name='en_weight_aux']").val() === '0.00') {
                                $("input[name='en_weight_aux']").select();
                            }
                            else{
                                // console.log('valor inicial ' + $("input[name='en_weight_aux']").val());
                                // console.log('nuevo valor ' + '0.00');
                                $("input[name='en_weight_aux']").val('0.00');
                                $("input[name='en_weight_aux']").select();
                            }
                        }
                    }
                });
            });
        },
    });

    widgetRegistry.add('st_weight_scale', StWeightScale);

    widgetRegistry.add('en_weight_scale', EnWeightScale);
});

