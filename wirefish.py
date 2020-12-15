def frame_decoder(frame_src: str) -> int:
    """
    Analyse la trame
    """
    # frame = open(frame_src, 'r')
    # res = open('./result.txt', 'w')

    buffer = ""
    out = ""
    print(ethernet_builder("00cb51d0aa8cc8d3ff4498380800"))
    print(ip_builder("45000208dc104000800605b2c0a801396813ed38"))
    print(tcp_builder("dd0a00509e5a0edbc12c15ee50180404b7150000"))
    # analyse_http("00 cb 51 d0 aa 8c c8 d3 ff 44 98 38 08 00")

    return 1


def ethernet_builder(seq: str) -> str:
    """
    Analyse le protocole Ethernet de la trame
    """
    if len(seq) < 14:
        print('Erreur: trame mal formatée')
        exit(1)

    ethernet_fields = {
    #   field_name: (b_size: int, val_format: str, get_opt: func, {sons})
        'Destination': (48, 'mac', None, {}),
        'Source': (48, 'mac', None, {}),
        'Type': (16, 'hex', None, {}),
    }

    return 'Ethernet II\n' + get_fields(ethernet_fields, seq)


def ip_builder(seq: str) -> str:
    """
    Analyse le protocole IP de la trame
    """

    ip_fields = {
    #   f_name: (b_size: int, val_format: str, get_opt: func, {sons})
        'Version': (4, 'hex', None, {}),
        'Header Length': (4, 'hex', None, {}),
        'Type of Service': (8, 'hex', None, {}),
        'Total Length': (16, 'hex', None, {}),
        'Identifier': (16, 'hex', None, {}),
        'Flags': (8, 'hex', None, {                     # TODO: size=3
            'Reserved bits': (1, 'hex', None, {}),
            'Don\'t fragment': (1, 'hex', None, {}),
            'More fragments': (1, 'hex', None, {}),
        }),
        'Fragment Offset': (8, 'hex', None, {}),        # TODO: size=13
        'Time to Live': (8, 'hex', None, {}),
        'Protocol': (8, 'hex', None, {}),
        'Header Checksum': (16, 'hex', None, {}),
        'Source IP Address': (32, 'ip4', None, {}),
        'Destination IP Address': (32, 'ip4', None, {}),
    }

    opt_size = (len(seq.replace(' ', ''))//2 - 20) * 8
    if opt_size > 0:
        ip_fields['Options'] = (opt_size, 'hex', None, {})

    return 'Internet Protocol (IP)\n' + get_fields(ip_fields, seq)


def tcp_builder(seq: str) -> str:
    """
    Analyse le protocole TCP de la trame
    """

    tcp_fields = {
    #   f_name: (b_size: int, val_format: str, get_opt: func, {sons})
        'Source Port': (16, 'hex', None, {}),
        'Destination Port': (16, 'hex', None, {}),
        'Sequence Number': (32, 'hex', None, {}),
        'Acknowledgment Number': (32, 'hex', None, {}),
        'Header Length': (4, 'hex', None, {}),
        'Flags': (12, 'hex', None, {
            'Reserved': (6, 'hex', None, {}),
            'Urgent': (1, 'hex', None, {}),
            'Acknowledgment': (1, 'hex', None, {}),
            'Push': (1, 'hex', None, {}),
            'Reset': (1, 'hex', None, {}),
            'Syn': (1, 'hex', None, {}),
            'Fin': (1, 'hex', None, {}),
        }),
        'Window': (16, 'hex', None, {}),
        'Checksum': (16, 'hex', None, {}),
        'Urgent Pointer': (16, 'hex', None, {}),
    }

    opt_size = (len(seq.replace(' ', ''))//2 - 20) * 8
    if opt_size > 0:
        tcp_fields['Options'] = (opt_size, 'hex', None, {})

    return 'Transmission Control Protocol (TCP)\n' + get_fields(tcp_fields, seq)



def http_builder(seq: str) -> str:
    """
    Analyse le protocole HTTP de la trame
    """
    pass



### UTILS ###

def get_fields(tr_fields: dict(), seq: str) -> str:
    out_str = ''    # decoder
    cursor = 0      # current index in the bytes sequence

    # for each field's name in the trace's fields
    for f_name in tr_fields:
        (b_size, v_format, get_opt, sons) = tr_fields[f_name]
        val, cursor = get_value(seq, cursor, b_size, v_format)
        out_str += '\t' + f_name + ': ' + val + '\n'
 
    return out_str


def get_value(seq: str, cursor: int, b_size: int, v_format: str) -> (str, int):
    n_cursor = cursor # next value of the cursor
    # TODO: gerer les champs de taille en bits impaire (ex: ToS) 
    # TODO: gerer les fils
    if b_size > 4:
        size = b_size//4    # size of the field in the seq
        eo_field = cursor + size    # end of the field index
        val = seq[cursor:eo_field] if eo_field < len(seq) else seq[-size:]
        n_cursor = eo_field
    else:
        val = seq[cursor]
        n_cursor = cursor + 1

    return format_val(val, v_format), n_cursor
    # return val, n_cursor


def format_val(val: str, v_format: str) -> str:
    formats = {
        'hex':  ('0x' + val),
        # TODO: 'bin':  val,
        'mac':  ':'.join(["".join(x) for x in zip(*[iter(val)]*2)]),
        'ip4':  '.'.join(str(x) for x in [int(x, 16) for x in
                [''.join(x) for x in zip(*[iter(val)]*2)]]),
    }

    return formats.get(v_format, val)

############



def main():
    frame_src = './trame_tcp'
    # print("Wirefish : Wireshark but worse.\n\n")
    if frame_decoder(''):
        # print("\n\nAnalyse terminée avec succès.")
        return 0
    # print("Analyse terminée avec erreur.")
    return 1

if __name__ == "__main__":
    main()