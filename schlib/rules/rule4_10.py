# -*- coding: utf-8 -*-

from rules.rule import *

class Rule(KLCRule):
    """
    Create the methods check and fix to use with the kicad lib files.
    """
    def __init__(self, component):
        super(Rule, self).__init__(component, 'Rule 4.10 - Part metadata', 'Part meta-data is filled in as appropriate')

    def check(self):
        """
        Proceeds the checking of the rule.
        The following variables will be accessible after checking:
            * only_datasheet_missing
        """

        self.only_datasheet_missing = False
        invalid_documentation = 0

        #check part itself
        if self.checkDocumentation(self.component.name, self.component.documentation, False, self.component.isGraphicSymbol() or self.component.isPowerSymbol()):
            invalid_documentation += 1

        #check all its aliases too
        if self.component.aliases:
            invalid = []
            for alias in self.component.aliases.keys():
                if self.checkDocumentation(alias, self.component.aliases[alias], True, self.component.isGraphicSymbol() or self.component.isPowerSymbol()):
                    invalid_documentation+=1

        return invalid_documentation > 0

    def checkDocumentation(self, name, documentation, alias=False, isGraphicOrPowerSymbol=False):
    
        errors = []
        warnings = []
    
        if not documentation:
            errors.append("Missing all documentation fields (description, keywords, datasheet)")
        elif (not documentation['description'] or
            not documentation['keywords'] or
            not documentation['datasheet']):

            if (not documentation['description']):
                errors.append("Missing DESCRIPTION field")
            if (not documentation['keywords']):
                errors.append("Missing KEYWORDS field")
            if (not isGraphicOrPowerSymbol) and (not documentation['datasheet']):
                errors.append("Missing DATASHEET field")
                
                if (documentation['description'] and
                    documentation['keywords']):
                    self.only_datasheet_missing = True

        elif name.lower() in documentation['description'].lower():
            warnings.append("Symbol name should not be included in description")
            
        if len(errors) > 0 or len(warnings) > 0:
            msg = "{cmp} {name} has metadata errors:".format(
                cmp = "ALIAS" if alias else "Component",
                name = name)
            if len(errors) == 0:
                self.warning(msg)
            else:
                self.error(msg)
                
            for err in errors:
                self.errorExtra(err)
            for warn in warnings:
                self.warningExtra(warn)
                
        return len(errors) > 0


    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """
        self.info("FIX: not supported" )
