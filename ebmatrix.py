import sys, subprocess, pprint

class EasyConfig(object):
    __slots__ = ('pkgname', 'pkgver', 'tc', 'tcver', 'other')
    def __init__(self, pkgname, pkgver, tc, tcver, other=''):
    
        self.pkgname = pkgname
        self.pkgver = pkgver
        self.tc = tc
        self.tcver = tcver
        self.other = other
    def __str__(self):
        parts = [self.pkgname, self.pkgver, self.tc, self.tcver] + ([self.other] if self.other else [])
        return '-'.join(parts)

def eb_search(pkgname):
    """ Return a sequence of EasyConfig objects given a package name (not a regex search as taken by `eb -S`) """
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
            ec = EasyConfig(pkg, pkg_ver, chain, chain_ver, rest)
            results.append(ec)

    return results

if __name__ == '__main__':
    packages = sys.argv[1:]
    
    # gather info about all packages
    results = {} # key-> toolchain-ver, value->[pkg, pkg, ...]
    for pkg in packages:
        
        ecs = eb_search(pkg)
        if not ecs:
            raise ValueError("No matches found for '%s'" % pkg)
        for ec in ecs:
            toolchain = '%s-%s' % (ec.tc, ec.tcver)
            if toolchain not in results:
                results[toolchain] = []
            results[toolchain].append(ec)
        
    #pprint.pprint(results)
    #print('---')
    
    # print matrix
    for tc in sorted(results.keys()):
        print(tc, end=' : ')
        for ec in results[tc]:
            print(ec, end=' : ')
        print()
    exit()
    
    print(all_tcs)
    exit()

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



        
        