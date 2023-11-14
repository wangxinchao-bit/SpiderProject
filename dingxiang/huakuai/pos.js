function e(n, i) {
    for (var e = [2, 1, 0], t = 0; ; ) {
        switch (e[t++]) {
        case 0:
            return !1;
        case 1:
            for (var r = 0, o = n.length; r < o; r++)
                if (n[r] === i)
                    return !0;
            continue;
        case 2:
            if (n.includes)
                return n.includes(i);
            continue
        }
        break
    }
}
function t(n) {
    if (!n)
        return "";
    for (var i = "", e = "V587", t = 49698, r = 0; r < n.length; r++) {
        var o = n.charCodeAt(r);
        o ^= e.charCodeAt(t = (t + 1) % 4),
        i += String.fromCharCode(o)
    }
    return i
}
function encrypy (n) {
    for (var i = [], r = 0; r < n.length; r++) {
        var o = n.charCodeAt(r);
        if (32 === r)
            break;
        for (; e(i, o % 32); )
            o++;
        i[t("G#FP")](o % 32)
    }
    return i
}
