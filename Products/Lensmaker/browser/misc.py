from Products.Five.browser import BrowserView
from zope.interface import implements
from interfaces import *
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from Products.CMFPlone import PloneMessageFactory as _
from Products.Lensmaker.config import TAGNAMESPACE_DELIMITER

class MiscView(BrowserView):

    implements(IMiscView)

    def objectifyTagNamespaceList(self, li, lens_path=None, return_dictionary=False):
        context = aq_inner(self.context)

        lc = getToolByName(context, 'lens_catalog')

        # If lens_path is not supplied the use path of context
        if lens_path is None:
            path = '/'.join(context.getPhysicalPath())
        else:
            path = lens_path
                    
        di = {}
        processed = []
        for item in li:
            # We split the namespace tags to get a prefix and term. The list
            # comprehension and trimming protects us from breaking if
            # delimiters are used in the prefix or term parts, which should not
            # happen after the validation steps.
            splitted = [part for part in item.split(TAGNAMESPACE_DELIMITER) if
                        part][:2]
            if len(splitted) == 1:
                continue
            prefix, term = splitted
            brains = lc(
                portal_type='TagNamespace',
                path=path,
                getPrefix=prefix,
             )
            if not brains:
                continue

            obj = brains[0].getObject()
            if obj not in processed:
                processed.append(obj)
            di.setdefault(obj, [])
        
            # Find the full tag (term + label).
            tag = ''
            for l_tag in obj.getTags():
                l_term = self.getNamespaceTagTerm(prefix='', tag=l_tag)
                if term == l_term:
                    tag = l_tag
                    break
            # Display only where tag is both available for lens and in li parameter
            if tag:
              di[obj].append(tag)

        if return_dictionary:
            return di

        # Convert into a list of dictionaries
        result = []
        for obj in processed:
            result.append({'tagnamespace':obj, 'tags':di[obj]})

        result.sort(lambda x,y: cmp(x['tagnamespace'].getId().lower(), 
                        y['tagnamespace'].getId().lower()))
        return result

    def getPrintableTags(self, tags, lens_path=None):
        result = []

        # Namespaced tags
        for di in self.objectifyTagNamespaceList(tags, lens_path=lens_path):
            for tag in di['tags']:
                result.append("%s" % self.getNamespaceTagTerm(prefix='', tag=tag))

        # Normal tags    
        for tag in tags:
            if tag.find(TAGNAMESPACE_DELIMITER) == -1:
                result.append(tag)

        return result

    def _getNamespaceTagTokens(self, tag):
        """
        Tokenize the tag string and return the term and label
        """
        li = tag.split(' ')
        if len(li) == 1:
            return li[0], li[0]
        return li[0], ' '.join(li[1:])

    def getNamespaceTagTerm(self, prefix, tag):
        term, label = self._getNamespaceTagTokens(tag)
        if prefix:
            return '%s%s%s' % (prefix, TAGNAMESPACE_DELIMITER, term)
        else:
            return term

    def getNamespaceTagLabel(self, tag):
        term, label = self._getNamespaceTagTokens(tag)
        return label.lstrip()

    def getTagNamespaceEditBatch(self):
        """
        From request, either create new object or 
        return objects from ids in batch
        """
        new_id = self.request.get('new_id', None)
        folder = self.context['tag-namespaces']
        if new_id is not None:
            ob = folder.restrictedTraverse( 
                    'portal_factory/TagNamespace/' + new_id)
            return [ob]
        else:
            return [folder[id] for id in self.request.selected_ids]

    def getLensContentTypeBreakdown(self, results):
        """
        Return a breakdown of the types in a lens
        """
        breakdown = {}
        for r in results:
            if not breakdown.has_key(r.portal_type):
                breakdown[r.portal_type] = 0
            breakdown[r.portal_type] += 1
        keys = breakdown.keys()
        keys.sort()
        output = ''
        for k in keys:
            if breakdown[k] == 1: betterk = k.lower()
            else:                 betterk = k.lower() + 's'
            output += '%d %s and ' % (breakdown[k], betterk)
        return output[:-5]

    def makeTagsDictFromTagsInUse(self, tags_in_use):
        return_di = {}
        
        if tags_in_use:
          for namespace in tags_in_use:
              ns = namespace['tagnamespace'].getPrefix()
              return_di[ns] = {}
              
              for tag in namespace['tags']:
                id = ''
                label = ''
                id, label = self._getNamespaceTagTokens(tag)
                return_di[ns][id] = label.lstrip()
        return return_di
