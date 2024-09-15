/** @odoo-module */


import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment } from "@web/core/utils/render";


export function _chunk(array, size) {
    var result = [];
    for (let i = 0; i < array.length; i += size) {
             result.push(array.slice(i, i + size));
    }
    return result;
    }


publicWidget.registry.snippet_clicking_page = publicWidget.Widget.extend({
    selector: '.container',
    events: {
        'click .snippet': '_onClickSnippet',
    },

    _onClickSnippet: function(e){
        var clicked_event_id = $(e.currentTarget).children().children().html()
        window.location = `/event/${clicked_event_id}`;
    },

});


var RecentEvents = publicWidget.Widget.extend({
    selector: '.recent_event_snippet',

    start: function () {
        jsonrpc('/recent-events', {}).then((result) => {
        const refEl = this.$el.find("#recent_events")
        $(result['recent_events']).each(function(){
            var description = $(this.description).text()
            this.description = description
        })
        var result = _chunk(result['recent_events'],4)
        result[0].is_active = true
        console.log(result)
        refEl.html(renderToFragment('school_management.recent_event_wise', {
            result,
        }))
        })
    },
});
publicWidget.registry.recent_event_wise_snippet = RecentEvents;
return RecentEvents;