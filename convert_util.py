class ConvertUtil:
    marker = ', '

    @classmethod
    def convert(cls, possibly_dict):
        def is_single_dict(given_item):
            return isinstance(given_item, dict) and len(given_item) == 1

        def get_list_output(input_list):
            if isinstance(input_list, dict):
                raise ValueError
            return cls.marker.join(ConvertUtil.convert(val)
                                   for val in input_list)

        if not (isinstance(possibly_dict, dict) or isinstance(possibly_dict, list)):
            return str(possibly_dict)

        if isinstance(possibly_dict, list):
            return '[' + get_list_output(possibly_dict) + ']'

        is_single = is_single_dict(possibly_dict)
        # I don't like this style...
        so_far = []
        for key, value in possibly_dict.items():
            if key in ['S', 'N', 'BOOL', 'NULL', 'M']:
                so_far += [ConvertUtil.convert(value)]
            elif key in ['SS', 'NS', 'BS']:
                so_far += ['{' + ConvertUtil.convert(value) + '}']
            elif key in ['L']:
                so_far += ['[' + get_list_output(value) + ']']
            else:
                so_far += [str(key) + ': ' + ConvertUtil.convert(value)]

        result = cls.marker.join(so_far)

        return '{' + result + '}' if not is_single else result

    @classmethod
    def convert_items(cls, dynamodb_item_response_list):
        '''
        :param dynamodb_item_response_list: list from DynamoDB response from the key 'Item'
        '''
        assert isinstance(dynamodb_item_response_list, list)

        for idx, given_dict in enumerate(dynamodb_item_response_list):
            converted = {key: ConvertUtil.convert(value)
                         for key, value in given_dict.items()}
            # Warning: inplace operation, not functional...
            dynamodb_item_response_list[idx] = converted

        return dynamodb_item_response_list
