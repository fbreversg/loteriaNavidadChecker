""" Logica del bot."""

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def add_number(user, number, amount):
    logger.debug("Add %s: %s / %s euros", user, number, amount)
    pass


def delete_number(user, number):
    logger.debug("Delete %s: %s", user, number)
    pass


def list_numbers(user):
    logger.debug("List %s", user)
    pass





