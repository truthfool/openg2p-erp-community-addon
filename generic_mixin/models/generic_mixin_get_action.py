from odoo import models, api


class GenericMixinGetAction(models.AbstractModel):
    """ This mixin provides method to read odoo action and optionaly
        replace context and domain of that action in result.

        Usage (if current model inherits from this mixin):

        def action_my_action(self):
            return self.get_action_by_xmlid(
                'my_action_xml_id',
                domain=[my domain],
                context=[my context],
            )


        Usage (if current model does not inherits from this mixin):

        def action_my_action(self):
            return self.env['generic.mixin.get.action'].get_action_by_xmlid(
                'my_action_xml_id',
                domain=[my domain],
                context=[my context],
            )

    """
    _name = 'generic.mixin.get.action'
    _description = "Generic Mixin: Get Action"
    # Note: this mixin is developed primaraly for compatability with 14.0

    @api.model
    def get_action_by_xmlid(self, xmlid, context=None, domain=None,
                            name=None):
        """ Simple method to get action by xmlid and update resulting dict with
            provided "update_data".

            In Odoo 14, the regular users have no access to ir.actions.*
            models, so, this method could be used to read action, and modify
            context and domain of resulting dict.

            :param str xmlid: XML (external) ID of action ir.actions.* to read
            :param dict context: apply new context for action
            :param list domain: apply new domain for action
            :param str name: apply new name for action
                (also changes display name)
            :return dict: Data for specified action
        """
        action = self.env.ref(xmlid)
        assert isinstance(  # nosec
            self.env[action._name], type(self.env['ir.actions.actions']))
        action = action.read()[0]
        if context is not None:
            action['context'] = context
        if domain is not None:
            action['domain'] = domain
        if name is not None:
            action['name'] = name
            action['display_name'] = name

        return action
