import sys, subprocess, pprint


def eb_search(pkgname):
    """ Return [pkg, pkg_ver, chain, chain_ver, rest] where rest may be '' """
    output = subprocess.run(['eb', '-S', pkgname], capture_output=True, text=True).stdout
    results = []
    for line in output.split('\n'): #  e.g. "* $CFGS1/h/HPL/HPL-2.3-intel-2019a.eb"
        line = line.split()
        if line and line[0] == '*' and line[1].endswith('.eb'):
            descr = line[-1].rsplit('/', 1)[-1].rsplit('.', 1)[0] # "HPL-2.3-intel-2019a.eb"
            # have to handle package names containing -, like "OSU-Micro-Benchmarks-5.3.2-foss-2016a"
            pkgparts = pkgname.split('-')
            nameparts = descr.split('-')
            pkg = '-'.join(nameparts.pop(0) for _ in pkgparts)
            if pkg != pkgname:
                continue
            pkg_ver = nameparts.pop(0)
            chain = nameparts.pop(0)
            chain_ver = nameparts.pop(0)
            rest = '.'.join(nameparts) # might be empty, so can't pop
            results.append([pkg, pkg_ver, chain, chain_ver, rest])

    return results

if __name__ == '__main__':
    packages = sys.argv[1:]
    
    # gather info about all packages
    data = []
    for pkg in packages:
        
        results = {}
        options = eb_search(pkg)
        if not options:
            raise ValueError("No matches found for '%s'" % pkg)
        for option in options:
            pkg, pkg_ver, chain, chain_ver, rest = option
            toolchain = '%s-%s' % (chain, chain_ver)
            if toolchain not in results:
                results[toolchain] = []
            results[toolchain].append(option)
        data.append(results)

    #pprint.pprint(data)
    #print('---')

    # find common toolchains
    if len(data) == 1:
        pass#exit()
    tc_sets = [set(d.keys()) for d in data]
    #print('tc_sets:', tc_sets)
    common = tc_sets[0]
    common.intersection_update(*tc_sets[1:])
    #print('common:',common)
    if len(common) > 1:
        print('Found %i common toolchains' % len(common))
        #print(common)
        for tc in common:
            print('%s:' % tc)
            for pkg in data:
                for match in pkg[tc]:
                    if match[-1] == '':
                        match.pop()
                    print(' ', '-'.join(match))
    else:
        print('No common toolchains found.')



        
        