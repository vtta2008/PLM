#!/usr/bin/env python
from PySide import QtCore, QtGui
import scenegraph_rc


ICONS = dict(    
    sizegrip                        = QtGui.QIcon(":/icons/icons/sizegrip.png"),
    checkbox_off                    = QtGui.QIcon(":/icons/icons/checkbox-off.png"),
    checkbox_on                     = QtGui.QIcon(":/icons/icons/checkbox-on.png"),
    spin_arrow_flat_down            = QtGui.QIcon(":/icons/icons/spin-arrow-flat-down.png"),
    spin_arrow_flat_up              = QtGui.QIcon(":/icons/icons/spin-arrow-flat-up.png"),
    arrow_flat_down                 = QtGui.QIcon(":/icons/icons/arrow-flat-down.png"),
    arrow_flat_left                 = QtGui.QIcon(":/icons/icons/arrow-flat-left.png"),
    arrow_flat_up                   = QtGui.QIcon(":/icons/icons/arrow-flat-up.png"),
    arrow_flat_right                = QtGui.QIcon(":/icons/icons/arrow-flat-right.png"),
    spin_arrow_flat_down_hover      = QtGui.QIcon(":/icons/icons/spin-arrow-flat-down-hover.png"),
    spin_arrow_flat_down_pressed    = QtGui.QIcon(":/icons/icons/spin-arrow-flat-down-pressed.png"),
    spin_arrow_flat_up_pressed      = QtGui.QIcon(":/icons/icons/spin-arrow-flat-up-pressed.png"),
    spin_arrow_flat_up_hover        = QtGui.QIcon(":/icons/icons/spin-arrow-flat-up-hover.png"),
    ui_dock_close_off               = QtGui.QIcon(":/icons/icons/ui-dock-close-off.png"),
    ui_dock_close_on                = QtGui.QIcon(":/icons/icons/ui-dock-close-on.png"),
    ui_dock_float_on                = QtGui.QIcon(":/icons/icons/ui-dock-float-on.png"),
    ui_dock_float_off               = QtGui.QIcon(":/icons/icons/ui-dock-float-off.png"),
    folder_horizontal_open          = QtGui.QIcon(":/icons/icons/folder-horizontal-open.png"),
    arrow_curve_000_double          = QtGui.QIcon(":/icons/icons/arrow-curve-000-double.png"),
    arrow_curve_000_left            = QtGui.QIcon(":/icons/icons/arrow-curve-000-left.png"),
    arrow_curve_090_left            = QtGui.QIcon(":/icons/icons/arrow-curve-090-left.png"),
    arrow_curve_090                 = QtGui.QIcon(":/icons/icons/arrow-curve-090.png"),
    arrow_curve_180_double          = QtGui.QIcon(":/icons/icons/arrow-curve-180-double.png"),
    arrow_curve_180_left            = QtGui.QIcon(":/icons/icons/arrow-curve-180-left.png"),
    arrow_curve_180                 = QtGui.QIcon(":/icons/icons/arrow-curve-180.png"),
    arrow_curve_270_left            = QtGui.QIcon(":/icons/icons/arrow-curve-270-left.png"),
    arrow_curve_270                 = QtGui.QIcon(":/icons/icons/arrow-curve-270.png"),
    arrow_curve                     = QtGui.QIcon(":/icons/icons/arrow-curve.png"),
    home                            = QtGui.QIcon(":/icons/icons/home.png"),
    information                     = QtGui.QIcon(":/icons/icons/information.png"),
    json                            = QtGui.QIcon(":/icons/icons/json.png"),
    network_cloud                   = QtGui.QIcon(":/icons/icons/network-cloud.png"),
    network_status_away             = QtGui.QIcon(":/icons/icons/network-status-away.png"),
    network_status_busy             = QtGui.QIcon(":/icons/icons/network-status-busy.png"),
    network_status_offline          = QtGui.QIcon(":/icons/icons/network-status-offline.png"),
    network_status                  = QtGui.QIcon(":/icons/icons/network-status.png"),
    node_delete_child               = QtGui.QIcon(":/icons/icons/node-delete-child.png"),
    node_delete_next                = QtGui.QIcon(":/icons/icons/node-delete-next.png"),
    node_delete_previous            = QtGui.QIcon(":/icons/icons/node-delete-previous.png"),
    node_delete                     = QtGui.QIcon(":/icons/icons/node-delete.png"),
    node_design                     = QtGui.QIcon(":/icons/icons/node-design.png"),
    node_insert_child               = QtGui.QIcon(":/icons/icons/node-insert-child.png"),
    node_insert_next                = QtGui.QIcon(":/icons/icons/node-insert-next.png"),
    node_insert_previous            = QtGui.QIcon(":/icons/icons/node-insert-previous.png"),
    node_insert                     = QtGui.QIcon(":/icons/icons/node-insert.png"),
    node_magnifier                  = QtGui.QIcon(":/icons/icons/node-magnifier.png"),
    node_select_all                 = QtGui.QIcon(":/icons/icons/node-select-all.png"),
    node_select_child               = QtGui.QIcon(":/icons/icons/node-select-child.png"),
    node_select_next                = QtGui.QIcon(":/icons/icons/node-select-next.png"),
    node_select_previous            = QtGui.QIcon(":/icons/icons/node-select-previous.png"),
    node_select                     = QtGui.QIcon(":/icons/icons/node-select.png"),
    node                            = QtGui.QIcon(":/icons/icons/node.png"),
    plug_arrow                      = QtGui.QIcon(":/icons/icons/plug--arrow.png"),
    plug_exclamation                = QtGui.QIcon(":/icons/icons/plug--exclamation.png"),
    plug_minus                      = QtGui.QIcon(":/icons/icons/plug--minus.png"),
    plug_pencil                     = QtGui.QIcon(":/icons/icons/plug--pencil.png"),
    plug_plus                       = QtGui.QIcon(":/icons/icons/plug--plus.png"),
    plug_connect                    = QtGui.QIcon(":/icons/icons/plug-connect.png"),
    plug_disconnect_prohibition     = QtGui.QIcon(":/icons/icons/plug-disconnect-prohibition.png"),
    plug_disconnect                 = QtGui.QIcon(":/icons/icons/plug-disconnect.png"),
    plug                            = QtGui.QIcon(":/icons/icons/plug.png"),
    status_away                     = QtGui.QIcon(":/icons/icons/status-away.png"),
    status_busy                     = QtGui.QIcon(":/icons/icons/status-busy.png"),
    status_offline                  = QtGui.QIcon(":/icons/icons/status-offline.png"),
    status                          = QtGui.QIcon(":/icons/icons/status.png"),
    terminal_arrow                  = QtGui.QIcon(":/icons/icons/terminal--arrow.png"),
    terminal_plus                   = QtGui.QIcon(":/icons/icons/terminal--plus.png"),
    terminal_medium                 = QtGui.QIcon(":/icons/icons/terminal-medium.png"),
    terminal_network                = QtGui.QIcon(":/icons/icons/terminal-network.png"),
    tick_circle                     = QtGui.QIcon(":/icons/icons/tick-circle.png"),
    toggle_small_expand             = QtGui.QIcon(":/icons/icons/toggle-small-expand.png"),
    toggle_small                    = QtGui.QIcon(":/icons/icons/toggle-small.png"),
    ui_accordion                    = QtGui.QIcon(":/icons/icons/ui-accordion.png"),
    ui_address_bar_green            = QtGui.QIcon(":/icons/icons/ui-address-bar-green.png"),
    ui_address_bar_lock             = QtGui.QIcon(":/icons/icons/ui-address-bar-lock.png"),
    ui_address_bar_red              = QtGui.QIcon(":/icons/icons/ui-address-bar-red.png"),
    ui_address_bar_yellow           = QtGui.QIcon(":/icons/icons/ui-address-bar-yellow.png"),
    ui_address_bar                  = QtGui.QIcon(":/icons/icons/ui-address-bar.png"),
    ui_breadcrumb_bread             = QtGui.QIcon(":/icons/icons/ui-breadcrumb-bread.png"),
    ui_breadcrumb_select_current    = QtGui.QIcon(":/icons/icons/ui-breadcrumb-select-current.png"),
    ui_breadcrumb_select_parent     = QtGui.QIcon(":/icons/icons/ui-breadcrumb-select-parent.png"),
    ui_breadcrumb_select            = QtGui.QIcon(":/icons/icons/ui-breadcrumb-select.png"),
    ui_breadcrumb                   = QtGui.QIcon(":/icons/icons/ui-breadcrumb.png"),
    ui_button_default               = QtGui.QIcon(":/icons/icons/ui-button-default.png"),
    ui_button_image                 = QtGui.QIcon(":/icons/icons/ui-button-image.png"),
    ui_button_navigation_back       = QtGui.QIcon(":/icons/icons/ui-button-navigation-back.png"),
    ui_button_navigation            = QtGui.QIcon(":/icons/icons/ui-button-navigation.png"),
    ui_button_toggle                = QtGui.QIcon(":/icons/icons/ui-button-toggle.png"),
    ui_button                       = QtGui.QIcon(":/icons/icons/ui-button.png"),
    ui_buttons                      = QtGui.QIcon(":/icons/icons/ui-buttons.png"),
    ui_check_box_mix                = QtGui.QIcon(":/icons/icons/ui-check-box-mix.png"),
    ui_check_box_uncheck            = QtGui.QIcon(":/icons/icons/ui-check-box-uncheck.png"),
    ui_check_box                    = QtGui.QIcon(":/icons/icons/ui-check-box.png"),
    ui_check_boxes_list             = QtGui.QIcon(":/icons/icons/ui-check-boxes-list.png"),
    ui_check_boxes_series           = QtGui.QIcon(":/icons/icons/ui-check-boxes-series.png"),
    ui_check_boxes                  = QtGui.QIcon(":/icons/icons/ui-check-boxes.png"),
    ui_color_picker_default         = QtGui.QIcon(":/icons/icons/ui-color-picker-default.png"),
    ui_color_picker_switch          = QtGui.QIcon(":/icons/icons/ui-color-picker-switch.png"),
    ui_color_picker_transparent     = QtGui.QIcon(":/icons/icons/ui-color-picker-transparent.png"),
    ui_color_picker                 = QtGui.QIcon(":/icons/icons/ui-color-picker.png"),
    ui_combo_box_blue               = QtGui.QIcon(":/icons/icons/ui-combo-box-blue.png"),
    ui_combo_box_calendar           = QtGui.QIcon(":/icons/icons/ui-combo-box-calendar.png"),
    ui_combo_box_edit               = QtGui.QIcon(":/icons/icons/ui-combo-box-edit.png"),
    ui_combo_box                    = QtGui.QIcon(":/icons/icons/ui-combo-box.png"),
    ui_combo_boxes                  = QtGui.QIcon(":/icons/icons/ui-combo-boxes.png"),
    ui_flow                         = QtGui.QIcon(":/icons/icons/ui-flow.png"),
    ui_group_box                    = QtGui.QIcon(":/icons/icons/ui-group-box.png"),
    ui_label_link                   = QtGui.QIcon(":/icons/icons/ui-label-link.png"),
    ui_label                        = QtGui.QIcon(":/icons/icons/ui-label.png"),
    ui_labels                       = QtGui.QIcon(":/icons/icons/ui-labels.png"),
    ui_layered_pane                 = QtGui.QIcon(":/icons/icons/ui-layered-pane.png"),
    ui_layout_panel                 = QtGui.QIcon(":/icons/icons/ui-layout-panel.png"),
    ui_list_box_blue                = QtGui.QIcon(":/icons/icons/ui-list-box-blue.png"),
    ui_list_box                     = QtGui.QIcon(":/icons/icons/ui-list-box.png"),
    ui_menu_blue                    = QtGui.QIcon(":/icons/icons/ui-menu-blue.png"),
    ui_menu                         = QtGui.QIcon(":/icons/icons/ui-menu.png"),
    ui_paginator                    = QtGui.QIcon(":/icons/icons/ui-paginator.png"),
    ui_panel_resize_actual          = QtGui.QIcon(":/icons/icons/ui-panel-resize-actual.png"),
    ui_panel_resize                 = QtGui.QIcon(":/icons/icons/ui-panel-resize.png"),
    ui_panel                        = QtGui.QIcon(":/icons/icons/ui-panel.png"),
    ui_progress_bar_indeterminate   = QtGui.QIcon(":/icons/icons/ui-progress-bar-indeterminate.png"),
    ui_progress_bar                 = QtGui.QIcon(":/icons/icons/ui-progress-bar.png"),
    ui_radio_button_uncheck         = QtGui.QIcon(":/icons/icons/ui-radio-button-uncheck.png"),
    ui_radio_button                 = QtGui.QIcon(":/icons/icons/ui-radio-button.png"),
    ui_radio_buttons_list           = QtGui.QIcon(":/icons/icons/ui-radio-buttons-list.png"),
    ui_radio_buttons                = QtGui.QIcon(":/icons/icons/ui-radio-buttons.png"),
    ui_ruler                        = QtGui.QIcon(":/icons/icons/ui-ruler.png"),
    ui_scroll_bar_horizontal        = QtGui.QIcon(":/icons/icons/ui-scroll-bar-horizontal.png"),
    ui_scroll_bar                   = QtGui.QIcon(":/icons/icons/ui-scroll-bar.png"),
    ui_scroll_pane_block            = QtGui.QIcon(":/icons/icons/ui-scroll-pane-block.png"),
    ui_scroll_pane_blog             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-blog.png"),
    ui_scroll_pane_both             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-both.png"),
    ui_scroll_pane_detail           = QtGui.QIcon(":/icons/icons/ui-scroll-pane-detail.png"),
    ui_scroll_pane_form             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-form.png"),
    ui_scroll_pane_horizontal       = QtGui.QIcon(":/icons/icons/ui-scroll-pane-horizontal.png"),
    ui_scroll_pane_icon             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-icon.png"),
    ui_scroll_pane_image            = QtGui.QIcon(":/icons/icons/ui-scroll-pane-image.png"),
    ui_scroll_pane_list             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-list.png"),
    ui_scroll_pane_table            = QtGui.QIcon(":/icons/icons/ui-scroll-pane-table.png"),
    ui_scroll_pane_text_image       = QtGui.QIcon(":/icons/icons/ui-scroll-pane-text-image.png"),
    ui_scroll_pane_text             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-text.png"),
    ui_scroll_pane_tree             = QtGui.QIcon(":/icons/icons/ui-scroll-pane-tree.png"),
    ui_scroll_pane                  = QtGui.QIcon(":/icons/icons/ui-scroll-pane.png"),
    ui_search_field                 = QtGui.QIcon(":/icons/icons/ui-search-field.png"),
    ui_seek_bar_050                 = QtGui.QIcon(":/icons/icons/ui-seek-bar-050.png"),
    ui_seek_bar_100                 = QtGui.QIcon(":/icons/icons/ui-seek-bar-100.png"),
    ui_seek_bar                     = QtGui.QIcon(":/icons/icons/ui-seek-bar.png"),
    ui_separator_label              = QtGui.QIcon(":/icons/icons/ui-separator-label.png"),
    ui_separator                    = QtGui.QIcon(":/icons/icons/ui-separator.png"),
    ui_slider_050                   = QtGui.QIcon(":/icons/icons/ui-slider-050.png"),
    ui_slider_100                   = QtGui.QIcon(":/icons/icons/ui-slider-100.png"),
    ui_slider_vertical_050          = QtGui.QIcon(":/icons/icons/ui-slider-vertical-050.png"),
    ui_slider_vertical_100          = QtGui.QIcon(":/icons/icons/ui-slider-vertical-100.png"),
    ui_slider_vertical              = QtGui.QIcon(":/icons/icons/ui-slider-vertical.png"),
    ui_slider                       = QtGui.QIcon(":/icons/icons/ui-slider.png"),
    ui_spacer                       = QtGui.QIcon(":/icons/icons/ui-spacer.png"),
    ui_spin                         = QtGui.QIcon(":/icons/icons/ui-spin.png"),
    ui_split_panel_vertical         = QtGui.QIcon(":/icons/icons/ui-split-panel-vertical.png"),
    ui_split_panel                  = QtGui.QIcon(":/icons/icons/ui-split-panel.png"),
    ui_splitter_horizontal          = QtGui.QIcon(":/icons/icons/ui-splitter-horizontal.png"),
    ui_splitter                     = QtGui.QIcon(":/icons/icons/ui-splitter.png"),
    ui_status_bar_blue              = QtGui.QIcon(":/icons/icons/ui-status-bar-blue.png"),
    ui_status_bar                   = QtGui.QIcon(":/icons/icons/ui-status-bar.png"),
    ui_tab_arrow                    = QtGui.QIcon(":/icons/icons/ui-tab--arrow.png"),
    ui_tab_exclamation              = QtGui.QIcon(":/icons/icons/ui-tab--exclamation.png"),
    ui_tab_minus                    = QtGui.QIcon(":/icons/icons/ui-tab--minus.png"),
    ui_tab_pencil                   = QtGui.QIcon(":/icons/icons/ui-tab--pencil.png"),
    ui_tab_plus                     = QtGui.QIcon(":/icons/icons/ui-tab--plus.png"),
    ui_tab_bottom                   = QtGui.QIcon(":/icons/icons/ui-tab-bottom.png"),
    ui_tab_content_vertical         = QtGui.QIcon(":/icons/icons/ui-tab-content-vertical.png"),
    ui_tab_content                  = QtGui.QIcon(":/icons/icons/ui-tab-content.png"),
    ui_tab_side                     = QtGui.QIcon(":/icons/icons/ui-tab-side.png"),
    ui_tab                          = QtGui.QIcon(":/icons/icons/ui-tab.png"),
    ui_text_area                    = QtGui.QIcon(":/icons/icons/ui-text-area.png"),
    ui_text_field_clear_button      = QtGui.QIcon(":/icons/icons/ui-text-field-clear-button.png"),
    ui_text_field_clear             = QtGui.QIcon(":/icons/icons/ui-text-field-clear.png"),
    ui_text_field_format            = QtGui.QIcon(":/icons/icons/ui-text-field-format.png"),
    ui_text_field_hidden            = QtGui.QIcon(":/icons/icons/ui-text-field-hidden.png"),
    ui_text_field_medium_select     = QtGui.QIcon(":/icons/icons/ui-text-field-medium-select.png"),
    ui_text_field_medium            = QtGui.QIcon(":/icons/icons/ui-text-field-medium.png"),
    ui_text_field_password_green    = QtGui.QIcon(":/icons/icons/ui-text-field-password-green.png"),
    ui_text_field_password_red      = QtGui.QIcon(":/icons/icons/ui-text-field-password-red.png"),
    ui_text_field_password_yellow   = QtGui.QIcon(":/icons/icons/ui-text-field-password-yellow.png"),
    ui_text_field_password          = QtGui.QIcon(":/icons/icons/ui-text-field-password.png"),
    ui_text_field_select            = QtGui.QIcon(":/icons/icons/ui-text-field-select.png"),
    ui_text_field_small_select      = QtGui.QIcon(":/icons/icons/ui-text-field-small-select.png"),
    ui_text_field_small             = QtGui.QIcon(":/icons/icons/ui-text-field-small.png"),
    ui_text_field_suggestion        = QtGui.QIcon(":/icons/icons/ui-text-field-suggestion.png"),
    ui_text_field                   = QtGui.QIcon(":/icons/icons/ui-text-field.png"),
    ui_toolbar_arrow                = QtGui.QIcon(":/icons/icons/ui-toolbar--arrow.png"),
    ui_toolbar_exclamation          = QtGui.QIcon(":/icons/icons/ui-toolbar--exclamation.png"),
    ui_toolbar_minus                = QtGui.QIcon(":/icons/icons/ui-toolbar--minus.png"),
    ui_toolbar_pencil               = QtGui.QIcon(":/icons/icons/ui-toolbar--pencil.png"),
    ui_toolbar_plus                 = QtGui.QIcon(":/icons/icons/ui-toolbar--plus.png"),
    ui_toolbar_bookmark             = QtGui.QIcon(":/icons/icons/ui-toolbar-bookmark.png"),
    ui_toolbar                      = QtGui.QIcon(":/icons/icons/ui-toolbar.png"),
    ui_tooltip_arrow                = QtGui.QIcon(":/icons/icons/ui-tooltip--arrow.png"),
    ui_tooltip_exclamation          = QtGui.QIcon(":/icons/icons/ui-tooltip--exclamation.png"),
    ui_tooltip_minus                = QtGui.QIcon(":/icons/icons/ui-tooltip--minus.png"),
    ui_tooltip_pencil               = QtGui.QIcon(":/icons/icons/ui-tooltip--pencil.png"),
    ui_tooltip_plus                 = QtGui.QIcon(":/icons/icons/ui-tooltip--plus.png"),
    ui_tooltip_balloon_bottom       = QtGui.QIcon(":/icons/icons/ui-tooltip-balloon-bottom.png"),
    ui_tooltip_balloon              = QtGui.QIcon(":/icons/icons/ui-tooltip-balloon.png"),
    ui_tooltip                      = QtGui.QIcon(":/icons/icons/ui-tooltip.png"),
    )


class IconMapper(object):
    def __init__(self, node=None):
        self.node = node


'''
# removing this for now, causes a QApplication error
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())
'''