import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .api import PGEEbokAPI

class PGEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api = PGEEbokAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            login_success = await api.login()
            
            if login_success:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], 
                    data=user_input
                )
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }), 
            errors=errors
        )